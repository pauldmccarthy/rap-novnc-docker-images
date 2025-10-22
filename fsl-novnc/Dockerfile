FROM  pauldmccarthy/ubuntu-novnc
LABEL org.opencontainers.image.authors="pauldmccarthy@gmail.com"
LABEL org.opencontainers.image.url="https://github.com/pauldmccarthy/rap-novnc-docker-images"
LABEL org.opencontainers.image.documentation="https://github.com/pauldmccarthy/rap-novnc-docker-images"
LABEL org.opencontainers.image.source="https://github.com/pauldmccarthy/rap-novnc-docker-images"
LABEL org.opencontainers.image.title="Ubuntu+noVNC desktop with FSL installed"
LABEL org.opencontainers.image.description="Ubuntu+noVNC desktop with FSL installed, for MRI image analysis on the UK Biobank Research Analysis Platform (RAP)."

#####
# FSL
#####

RUN GETFSL_URL=https://fsl.fmrib.ox.ac.uk/fsldownloads/fslconda/releases/getfsl.sh; \
    curl -Ls ${GETFSL_URL} | sh -s /opt/fsl                     && \
    echo 'export FSLDIR=/opt/fsl/'             >> /root/.bashrc && \
    echo 'source ${FSLDIR}/etc/fslconf/fsl.sh' >> /root/.bashrc
