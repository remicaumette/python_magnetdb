FROM trophime/magnettools:latest-poetry

#ENV TZ=Europe/Paris
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 DEBIAN_FRONTEND=noninteractive
RUN echo 'debconf debconf/frontend select Noninteractive' | sudo debconf-set-selections

USER root
#RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update \
    && apt-get install -y wait-for-it \
    && apt-get install -y debconf-utils \
    && apt-get install -y libxft2 libglu1 wget build-essential libseccomp-dev pkg-config squashfs-tools cryptsetup runc \
    && apt-get install -y python3-watchdog \
    && wget -q https://github.com/sylabs/singularity/releases/download/v3.10.0/singularity-ce_3.10.0-focal_amd64.deb \
    && dpkg -i singularity-ce_3.10.0-focal_amd64.deb \
    && rm -f singularity-ce_3.10.0-focal_amd64.deb
    
USER feelpp

