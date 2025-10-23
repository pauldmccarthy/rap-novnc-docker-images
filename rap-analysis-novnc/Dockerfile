FROM  pauldmccarthy/fsl-novnc
LABEL org.opencontainers.image.authors="pauldmccarthy@gmail.com"
LABEL org.opencontainers.image.url="https://github.com/pauldmccarthy/rap-novnc-docker-images"
LABEL org.opencontainers.image.documentation="https://github.com/pauldmccarthy/rap-novnc-docker-images"
LABEL org.opencontainers.image.source="https://github.com/pauldmccarthy/rap-novnc-docker-images"
LABEL org.opencontainers.image.title="Ubuntu+noVNC desktop with FSL, Connectome Workbench, and MATLAB installed"
LABEL org.opencontainers.image.description="Ubuntu+noVNC desktop with FSL, Connectome Workbench, and MATLAB installed, for MRI image analysis on the UK Biobank Research Analysis Platform (RAP)."

#######
# emacs
#######

RUN apt update -y        && \
    apt install -y emacs && \
    apt -y clean         && \
    apt -y autoremove    && \
    rm -rf /var/lib/apt/lists/*

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

######################
# Connectome Workbench
######################

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

RUN WBURL=https://humanconnectome.org/storage/app/media/workbench/workbench-linux64-v2.1.0.zip; \
    cd /opt/                                        && \
    curl -Ls ${WBURL} > workbench.zip               && \
    unzip workbench.zip                             && \
    rm ./workbench.zip                              && \
    rm -r workbench/libs_linux64_software_opengl    && \
    rm -r workbench/libs_linux64                    && \
    rm -r workbench/bin_linux64                     && \
    echo 'export PATH=/opt/workbench/exe_linux64:$PATH' >> /root/.bashrc

########
# MATLAB
########

# Pilfered from the following official Matlab docker image resources:
#  - https://github.com/mathworks-ref-arch/container-images/tree/main/matlab-deps/r2025b/ubuntu24.04
#  - https://github.com/mathworks-ref-arch/container-images/blob/main/matlab/Dockerfile

# Dependencies
RUN apt -y update                   && \
    apt install -y                     \
        apt-utils                      \
        ca-certificates                \
        debianutils                    \
        gcc-12                         \
        g++-12                         \
        ibverbs-providers              \
        libasound2t64                  \
        libatk-bridge2.0-0t64          \
        libatk1.0-0t64                 \
        libatomic1                     \
        libatspi2.0-0t64               \
        libc6                          \
        libcairo-gobject2              \
        libcairo2                      \
        libcap2                        \
        libcrypt1                      \
        libcups2t64                    \
        libdrm2                        \
        libfontconfig1                 \
        libfribidi0                    \
        libgbm1                        \
        libgdk-pixbuf-2.0-0            \
        libgl1                         \
        libglib2.0-0t64                \
        libgstreamer-plugins-base1.0-0 \
        libgstreamer1.0-0              \
        libgtk-3-0t64                  \
        libibverbs1                    \
        libice6                        \
        libltdl7                       \
        libnspr4                       \
        libnss3                        \
        libnuma1                       \
        libpam0g                       \
        libpango-1.0-0                 \
        libpangocairo-1.0-0            \
        libpangoft2-1.0-0              \
        libpixman-1-0                  \
        libpsm2-2                      \
        librdmacm1t64                  \
        libsndfile1                    \
        libtirpc3t64                   \
        libucx0                        \
        libuhd4.6.0-dpdk               \
        libuuid1                       \
        libxcomposite1                 \
        libxcursor1                    \
        libxdamage1                    \
        libxfixes3                     \
        libxfont2                      \
        libxft2                        \
        libxinerama1                   \
        libxrandr2                     \
        libxt6t64                      \
        libxtst6                       \
        libxxf86vm1                    \
        locales                        \
        locales-all                    \
        make                           \
        net-tools                      \
        procps                         \
        sudo                           \
        unzip                          \
        wget                           \
        x11-xkb-utils                  \
        zlib1g                      && \
        apt -y clean                && \
        apt -y autoremove           && \
        rm -rf /var/lib/apt/lists/*
RUN ln -s $(which gcc-12) /usr/bin/gcc && \
    ln -s $(which g++-12) /usr/bin/g++

# MATLAB itself
RUN cd /tmp/                                            && \
    curl -LsO https://www.mathworks.com/mpm/glnxa64/mpm && \
    chmod +x mpm                                        && \
    ./mpm install                                          \
        --release=r2025b                                   \
        --destination=/opt/MATLAB                          \
        --products "MATLAB"                             && \
    rm -f /opt/MATLAB/sys/os/glnxa64/libstdc++.*        && \
    rm -f mpm mathworks_root.log                        && \
    echo 'export PATH=/opt/MATLAB/bin:$PATH' >> /root/.bashrc

# Matlab Service Host
RUN MSHURL=https://www.mathworks.com/MathWorksServiceHost/glnxa64/install_managed_msh.sh; \
    cd /tmp/                                       && \
    curl  -Ls  ${MSHURL} > msh                     && \
    chmod +x ./msh                                 && \
    ./msh --destination /opt/Mathworks/ServiceHost && \
    rm ./msh

# Desktop file
ADD MATLAB.desktop /root/Desktop/
