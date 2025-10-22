FROM  ubuntu:24.04
LABEL org.opencontainers.image.authors="pauldmccarthy@gmail.com"
LABEL org.opencontainers.image.url="https://github.com/pauldmccarthy/rap-novnc-docker-images"
LABEL org.opencontainers.image.documentation="https://github.com/pauldmccarthy/rap-novnc-docker-images"
LABEL org.opencontainers.image.source="https://github.com/pauldmccarthy/rap-novnc-docker-images"
LABEL org.opencontainers.image.title="Minimal Ubuntu+noVNC desktop"
LABEL org.opencontainers.image.description="Minimual Ubuntu+noVNC installation for running software within a graphical Linux desktop environment. Includes the DNANexus 'dx' command-line tool for running on the UK Biobank Research Analysis Platform (RAP)."

###############################
# Core utilities + XFCE desktop
###############################

RUN DEBIAN_FRONTEND=noninteractive  && \
    apt update -y                   && \
    apt install -y locales          && \
    locale-gen en_US.UTF-8          && \
    locale-gen en_GB.UTF-8          && \
    update-locale                   && \
    apt install -y                     \
        bzip2                          \
        curl                           \
        dbus-x11                       \
        git                            \
        libxfce4ui-utils               \
        nano                           \
        python3                        \
        thunar                         \
        tigervnc-common                \
        tigervnc-standalone-server     \
        unzip                          \
        xfce4-appfinder                \
        xfce4-panel                    \
        xfce4-session                  \
        xfce4-settings                 \
        xfce4-terminal                 \
        xfconf                         \
        xfdesktop4                     \
        xfwm4                          \
        zip                         && \
        apt -y clean                && \
        apt -y autoremove           && \
        rm -rf /var/lib/apt/lists/* && \
        ln -s /usr/bin/python3 /usr/bin/python

#######
# noVNC
#######

RUN NOVNCURL=https://github.com/novnc/noVNC/archive/v1.6.0.tar.gz;         \
    WSCKURL=https://github.com/novnc/websockify/archive/v0.13.0.tar.gz;    \
    mkdir -p /opt/noVNC/utils/websockify                                && \
    cd /opt/noVNC/                                                      && \
    curl -sSfL ${NOVNCURL} | tar -zxf - --strip=1                       && \
    curl -sSfL ${WSCKURL}  | tar -zxf - -C ./utils/websockify --strip=1 && \
    find . -name ".git*"   | xargs rm -rf

RUN mkdir -p         /root/.vnc/
ADD vncserver-config /root/.vnc/config
ADD defaults.json    /opt/noVNC/
ADD startvnc         /opt/noVNC/startvnc
RUN chmod a+x        /opt/noVNC/startvnc

#################
# micromamba + dx
#################

RUN if   [ $(uname -m) = "x86_64" ]; then                                            \
      MMURL=https://micro.mamba.pm/api/micromamba/linux-64/latest;                   \
    elif [ $(uname -m) = "aarch64" ]; then                                           \
      MMURL=https://micro.mamba.pm/api/micromamba/linux-aarch64/latest;              \
    fi;                                                                              \
    export MAMBA_ROOT_PREFIX=/opt/micromamba;                                        \
    mkdir ${MAMBA_ROOT_PREFIX}                                                    && \
    cd ${MAMBA_ROOT_PREFIX}                                                       && \
    curl -Ls ${MMURL} | tar -xvj bin/micromamba                                   && \
    eval "$(bin/micromamba shell hook -s posix)"                                  && \
    micromamba activate ${MAMBA_ROOT_PREFIX}                                      && \
    bin/micromamba install -y -c conda-forge -p ${MAMBA_ROOT_PREFIX} python=3.12  && \
    bin/micromamba clean --all                                                    && \
    bin/pip install dxpy;

###############
# shell profile
###############

# Base env is activated by default. We also
# always want dx to be on the PATH, so we
# explicitly add /opt/micromamba/bin/.
RUN echo 'export MAMBA_ROOT_PREFIX=/opt/micromamba/'                        >> /root/.bashrc
RUN echo 'export PATH=/opt/micromamba/bin/:$PATH'                           >> /root/.bashrc
RUN echo 'eval "$(${MAMBA_ROOT_PREFIX}bin/micromamba shell hook -s posix)"' >> /root/.bashrc
RUN echo 'micromamba activate ${MAMBA_ROOT_PREFIX}'                         >> /root/.bashrc

ENV USER=root
WORKDIR /root

ENTRYPOINT [ "/opt/noVNC/startvnc" ]