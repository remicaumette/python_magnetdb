FROM trophime/magnettools:poetry

RUN sudo apt-get update
RUN sudo apt-get install -y libxft2 libglu1
RUN pip install watchdog