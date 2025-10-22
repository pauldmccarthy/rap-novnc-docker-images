FROM  pauldmccarthy/ubuntu-novnc
LABEL org.opencontainers.image.authors="pauldmccarthy@gmail.com"
LABEL org.opencontainers.image.url="https://github.com/pauldmccarthy/rap-novnc-docker-images"
LABEL org.opencontainers.image.documentation="https://github.com/pauldmccarthy/rap-novnc-docker-images"
LABEL org.opencontainers.image.source="https://github.com/pauldmccarthy/rap-novnc-docker-images"
LABEL org.opencontainers.image.title="Ubuntu+noVNC desktop with FSLeyes installed"
LABEL org.opencontainers.image.description="Ubuntu+noVNC desktop with FSLeyes and a few basic FSL utilities installed, for MRI image visualisation on the UK Biobank Research Analysis Platform (RAP)."

######################
# FSLeyes and fslmaths
######################

RUN /opt/micromamba/bin/micromamba create -y                        \
        -c https://fsl.fmrib.ox.ac.uk/fsldownloads/fslconda/public/ \
        -c conda-forge                                              \
        -p /opt/fsleyes/                                            \
        fsleyes fsl-avwutils fsl-data_standard fsl-data_atlases  && \
    /opt/micromamba/bin/micromamba clean --all                   && \
    echo 'micromamba activate /opt/fsleyes'    >> /root/.bashrc  && \
    echo 'export FSLDIR=/opt/fsleyes'          >> /root/.bashrc  && \
    echo 'source ${FSLDIR}/etc/fslconf/fsl.sh' >> /root/.bashrc
