#!/usr/bin/env python

import sys
import os.path as op
import textwrap as tw

import jinja2 as j2

BASEDIR = op.dirname(op.abspath(__file__))


def apt_install(*packages):
    pre = ['RUN DEBIAN_FRONTEND=noninteractive && \\',
           '    apt update -y && \\',
           '    apt install -y \\']

    packages      = list(packages)
    packages[:-1] = [f'        {p} \\' for p in packages[:-1]]
    packages[ -1] =  f'        {packages[-1]} && \\'

    post = ['    apt -y clean && \\',
            '    apt -y autoremove && \\',
            '    rm -rf /var/lib/apt/lists/*']

    return '\n'.join(pre + packages + post)


def add_to_profile(line):
    return f"RUN echo '{line}' >> /home/ubuntu/.bashrc"


def install_launcher(title, exe, icon, **envvars):

    basename    = title.replace(' ', '-')
    appfile     = f'/usr/share/applications/{basename}.desktop'
    desktopfile = f'/home/ubuntu/Desktop/{basename}.desktop'
    envvars     = ' '.join(f'{k}="{v}"' for k, v in envvars.items())
    desktop     = tw.dedent(f"""
    [Desktop Entry]
    Type=Application
    Name={title}
    Exec=env {envvars} {exe}
    Icon={icon}
    Terminal=false
    StartupNotify=false
    Path=/home/ubuntu/
    """).strip().replace('\n', '\\n')

    return tw.dedent(f"""
    RUN echo '{desktop}' > {appfile}   && \\
        chmod a+x {appfile}            && \\
        mkdir -p /home/ubuntu/Desktop  && \\
        rm -f {desktopfile}            && \\
        ln -s {appfile} {desktopfile}  && \\
        chown -R ubuntu:ubuntu /home/ubuntu/Desktop/
    """)

def generate_dockerfile(subdir):

    infile      = f'{subdir}/Dockerfile.jinja2'
    outfile     = f'{subdir}/Dockerfile'
    templatedir = f'{BASEDIR}/templates'

    loader = j2.FileSystemLoader([subdir, templatedir])
    jenv   = j2.Environment(loader=loader)
    env    = {
        'apt_install'      : apt_install,
        'add_to_profile'   : add_to_profile,
        'install_launcher' : install_launcher,
    }

    with open(infile, 'rt') as f:
        template = jenv.from_string(f.read())

    rendered = template.render(**env)

    with open(outfile, 'wt') as f:
        f.write(rendered)


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    if len(args) != 1:
        print('Usage: ')
        print()
        print('generate.py <sub-dir>')
        print()
        print('Or to build all images:')
        print()
        print('generate.py all')
        exit(1)

    if args[0] == 'all':
        subdirs = [
            'f{BASEDIR}/ubuntu-novnc',
            'f{BASEDIR}/fsleyes-novnc',
            'f{BASEDIR}/workbench-novnc',
            'f{BASEDIR}/fsl-novnc',
            'f{BASEDIR}/rap-analysis-novnc']
    else:
        subdirs = args

    subdirs = [op.abspath(s) for s in subdirs]

    for subdir in subdirs:
        print(f'Generating {subdir}/Dockerfile')
        generate_dockerfile(subdir)


if __name__ == '__main__':
    main()
