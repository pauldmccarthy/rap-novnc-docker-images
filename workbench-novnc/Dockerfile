FROM  pauldmccarthy/ubuntu-novnc
LABEL org.opencontainers.image.authors="pauldmccarthy@gmail.com"
LABEL org.opencontainers.image.url="https://github.com/pauldmccarthy/rap-novnc-docker-images"
LABEL org.opencontainers.image.documentation="https://github.com/pauldmccarthy/rap-novnc-docker-images"
LABEL org.opencontainers.image.source="https://github.com/pauldmccarthy/rap-novnc-docker-images"
LABEL org.opencontainers.image.title="Ubuntu+noVNC desktop with Connectome Workbench installed"
LABEL org.opencontainers.image.description="Ubuntu+noVNC desktop with Connectome Workbench, for MRI image analysis on the UK Biobank Research Analysis Platform (RAP)."

################
# Workbench deps
################

# The shared libraries bundled with
# workbench are out-dated, so we
# install them using apt, and remove
# the bundled copies.

RUN apt update -y       && \
    apt install -y         \
    libftgl2               \
    libglu1-mesa           \
    libosmesa6             \
    libqt5core5t64         \
    libqt5gui5t64          \
    libqt5network5t64      \
    libqt5opengl5t64       \
    libqt5printsupport5t64 \
    libqt5widgets5t64      \
    libqt5xml5t64       && \
    apt -y clean        && \
    apt -y autoremove   && \
    rm -rf /var/lib/apt/lists/*

######################
# Connectome workbench
######################

RUN WBURL=https://humanconnectome.org/storage/app/media/workbench/workbench-linux64-v2.1.0.zip; \
    cd /opt/                                        && \
    curl -Ls ${WBURL} > workbench.zip               && \
    unzip workbench.zip                             && \
    rm ./workbench.zip                              && \
    rm -r workbench/libs_linux64_software_opengl    && \
    rm -r workbench/libs_linux64                    && \
    rm -r workbench/bin_linux64                     && \
    echo 'export PATH=/opt/workbench/exe_linux64:$PATH' >> /root/.bashrc

