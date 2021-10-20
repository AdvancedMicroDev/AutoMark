FROM ubuntu:20.04

ENV LANG C.UTF-8
RUN apt-get upgrade && apt-get install -y python3.9 python3-pip virtualenv
RUN apt-get install -y vim
RUN pip install setuptools pip --upgrade --force-reinstall
RUN apt-get install -y python3-pip
RUN pip3 install torch
RUN pip3 install torchvision
RUN pip3 install opencv-python
RUN apt-get upgrade && apt-get install -y libsm6 libxext6 libxrender-dev
COPY . /app
WORKDIR /app

RUN mkdir /app/uploads
RUN pip3 install Flask

EXPOSE 5000

ENTRYPOINT ["python3.9", "server.py"]