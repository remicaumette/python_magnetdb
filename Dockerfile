FROM trophime/magnettools:poetry

ENV DEBIAN_FRONTEND=noninteractive
RUN echo 'debconf debconf/frontend select Noninteractive' | sudo debconf-set-selections

RUN sudo apt-get update
RUN sudo apt-get install -y debconf-utils
RUN sudo apt-get install -y libxft2 libglu1 wget build-essential libseccomp-dev pkg-config squashfs-tools cryptsetup runc
RUN pip install watchdog
RUN wget https://github.com/sylabs/singularity/releases/download/v3.10.0/singularity-ce_3.10.0-focal_amd64.deb
RUN sudo dpkg -i singularity-ce_3.10.0-focal_amd64.deb
