FROM ubuntu:latest

RUN apt update
RUN apt upgrade



# requirements
RUN apt install ffmpeg
RUN apt install git
RUN apt install python3
RUN apt install python3-pip

# python requirements
# copy requirements.txt
# install requirements.txt

