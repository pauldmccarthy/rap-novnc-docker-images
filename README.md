# noVNC Docker images for use on the UK Biobank RAP

This repository contains a collection of Docker image definitions for use on the [UK Biobank Research Analysis Platform (RAP)](https://www.ukbiobank.ac.uk/use-our-data/research-analysis-platform/). These images have been designed to ease the installation and use of custom graphical software on the RAP.

Each of the images:

 - Provide a minimul Ubuntu system.
 - Have the XFCE desktop environmnt installed.
 - Run [noVNC](https://github.com/novnc/noVNC/) for web browser-based access to the desktop.
 - Have [`micromamba`](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html) installed, which you can use to install software from the [Anaconda package repositories](https://anaconda.org/).
 - Have the [`dx`](https://documentation.dnanexus.com/user/helpstrings-of-sdk-command-line-utilities) command-line tool for access to your RAP project workspace.

The images are currently published to Docker Hub at <https://hub.docker.com/u/pauldmccarthy/>.

The following images are currently available:
 - `pauldmccarthy/ubuntu-novnc`: Minimal Ubuntu desktop without much else.
 - `pauldmccarthy/fsleyes-novnc`: Ubuntu desktop with the [FSLeyes image viewer](https://fsl.fmrib.ox.ac.uk/fsl/docs/utilities/fsleyes.html) and a few basic [FSL](https://fsl.fmrib.ox.ac.uk/fsl/docs/) utilities installed (`fslmaths`, `fslstats`, etc).
 - `pauldmccarthy/workbench-novnc`: Ubuntu desktop with [Connectome Workbench](https://humanconnectome.org/software/connectome-workbench), providing the `wb_command` and `wb_view` commands for NIfTI/CIfTI image analysis and visualisation.
 - `pauldmccarthy/fsl-novnc`: Ubuntu desktop with a full FSL installation for MRI analysis and visualisation.
 - `pauldmccarthy/rap-analysis-novnc`: Ubuntu desktop with FSL, [PANDORA](https://biobank.ndph.ox.ac.uk/ukb/label.cgi?id=539), Connectome Workbench, and MATLAB (you will need a MATLAB license in order to use MATLAB).


## Run locally

If you have Docker installed locally, you can run these images on your own computer using a command such as:

```bash
docker run --network host <image>:latest
```

where `<image>` is the image you want to use (e.g. `pauldmccarthy/fsleyes-novnc`).

Once the container has started running, open <http://localhost:8080/vnc.html?host=localhost&port=8080> in a web browser to access the desktop session. You can use `apt` and `micromamba` to install whatever software you need.


## Run on the UK Biobank RAP

You can use these images on the RAP via the _ttyd_ tool.

1.  Log into the RAP portal at <https://ukbiobank.dnanexus.com/login>.

2.  Click on _Tools_  at the top, and select _Tools Library_.

3.  Find and click on the _ttyd_ app (it may not be on the first page).

4.  Click the  _Run_ button at the top.

5.  Set _Output to_ to a location within the RAP project workspace you wish to work within, and click _Next_.

6.  Click the _Start Analysis_ button at the top-right.

7.  Click _Edit Instance Type_ to select your RAM/CPU resources.

8.  Click the _Launch Analysis_ button.

9.  You will be taken to the _Monitor_ page - click on the new entry corresponding to your new _ttyd_ session.

10. You will need to wait several minutes for the session to start up. When it is ready, click the _Open Worker URL_ link. This wil open a new web browser tab with a UNIX shell.

11. Run these commands in the shell (change `<image>` to the Docker image you wish to run, e.g. `pauldmccarthy/fsleyes-novnc`):
    ```bash
    env | egrep "^DX_" > dx.env
    docker run --network host      \
      --env-file dx.env            \
      -v /mnt/project:/mnt/project \
      <image>:latest
    ```

12. Once the image has started running, a message starting with _Open this URL in a web browser_ will be printed. Copy+paste the URL into a new web browser window to open your desktop session.

### Access your UK Biobank data

When running on the RAP, we recommend running the Docker image with commands such as:

```bash
env | egrep "^DX_" > dx.env
docker run --network host      \
  --env-file dx.env            \
  -v /mnt/project:/mnt/project \
  pauldmccarthy/ubuntu-novnc
```

The Docker images have the `dx` command installed, however in order for it to work correctly, you need to pass the relevant environment variables from the _ttyd_ session into the running Docker container. You can do this by saving them to a file, and then passing that file to `docker run` via its `--env-file` option. You may also need to re-select your RAP project by running:

```bash
dx select
```

Once this has been done, you can use `dx` to upload/download data to/from your RAP workspace:

 - `dx ls` - list the contents of your project workspace.
 - `dx download <file>` - download a file from your project workspace to the workstation.
 - `dx upload <file>` - upload a file from the workstation to your project workspace.

Within the _ttyd_ session, your RAP project workspace is also mounted (read-only) at `/mnt/project/` - in the above `docker run` command, this is mounted into the Docker container via the `-v` option. This means you can access your Project files without having to run `dx download`.


## Build your own Docker images


If you want to use some other graphical software on the RAP, you can build your own Docker image using the same strategy that is used here. In your own `Dockerfile` you can use the `pauldmccarthy/ubuntuc-novnc` image as a base, and then simply add the commands to install your software. Or feel free to copy+paste the contents of the `Dockerfile` files contained in this repository into your own `Dockerfile`.


## Licenses


The Docker images built from the files in this repository contain software and data covered by a range of different licenses:

 - FSLeyes: https://git.fmrib.ox.ac.uk/fsl/fsleyes/fsleyes/-/blob/main/LICENSE
 - FSL: https://fsl.fmrib.ox.ac.uk/fsl/docs/license.html
 - Workbench: https://github.com/Washington-University/workbench/blob/master/LICENSE
 - MATLAB: https://uk.mathworks.com/pricing-licensing.html
 - `dxpy`: https://github.com/dnanexus/dx-toolkit/blob/master/COPYING
 - noVNC: https://github.com/novnc/noVNC/blob/master/LICENSE.txt
 - Latest versions of the Human Connectome Project MSM surface averages included with permission from Matthew Glasser.


## Notes for development

All images are built using GitHub Actions via a manually triggered workflow.
To re-build an image locally, you can just run the `build.sh` script from the repository root, e.g.:

```bash
./build.sh ./ubuntu-novnc
```

The `build.sh` script assumes that you a `python` executable on your `$PATH` with the `jinja2` library installed.
