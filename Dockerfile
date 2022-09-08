FROM ubuntu:latest

RUN apt update
RUN apt upgrade



# requirements
RUN apt install ffmpeg
RUN apt install git
RUN apt install python3
RUN apt install python3-pip

# install chrome
RUN apt install wget
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb
RUN apt -f install
RUN dpkg -i google-chrome-stable_current_amd64.deb


# python requirements
# copy requirements.txt
# install requirements.txt

