FROM  pauldmccarthy/fsl-novnc
LABEL org.opencontainers.image.authors="pauldmccarthy@gmail.com"
LABEL org.opencontainers.image.url="https://github.com/pauldmccarthy/rap-novnc-docker-images"
LABEL org.opencontainers.image.documentation="https://github.com/pauldmccarthy/rap-novnc-docker-images"
LABEL org.opencontainers.image.source="https://github.com/pauldmccarthy/rap-novnc-docker-images"
LABEL org.opencontainers.image.title="Ubuntu+noVNC desktop with FSL and Connectome Workbench installed"
LABEL org.opencontainers.image.description="Ubuntu+noVNC desktop with FSL and Connectome Workbench installed, for MRI image analysis on the UK Biobank Research Analysis Platform (RAP)."

############################
# PANDORA version of fsl_glm
# and fastconfounds
############################

RUN /opt/fsl/bin/micromamba create -y                                    \
        --override-channels                                              \
        -c https://fsl.fmrib.ox.ac.uk/fsldownloads/fslconda/development/ \
        -c https://fsl.fmrib.ox.ac.uk/fsldownloads/fslconda/public/      \
        -c conda-forge                                                   \
        -p /opt/fsl/envs/pandora                                         \
        fsl-melodic fsl-fastconfounds                                 && \
    /opt/fsl/bin/micromamba clean --all

###################################
# Re-generate fsl_glm wrapper so it
# points to the pandora version
###################################

RUN FSLDIR=/opt/fsl/                         \
    PREFIX=/opt/fsl/envs/pandora/            \
    /opt/fsl/bin/python                      \
    /opt/fsl/share/fsl/sbin/createFSLWrapper \
        --force                              \
        --srcdir=/opt/fsl/envs/pandora/bin/  \
        --destdir=/opt/fsl/share/fsl/bin/    \
        fsl_glm fastconfounds

#######################################
# Workbench deps, emacs and web browser
#######################################

# The shared libraries bundled with
# workbench are out-dated, so we
# install them using apt, and remove
# the bundled copies.

RUN apt update -y       && \
    apt install -y         \
    emacs                  \
    firefox                \
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
