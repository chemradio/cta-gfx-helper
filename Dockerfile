FROM --platform=linux/amd64 ubuntu:latest

RUN apt update
RUN apt upgrade

# requirements
RUN apt install -y ffmpeg
RUN apt install -y git
RUN apt install -y python3
RUN apt install -y python3-pip

# install chrome
RUN apt install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install -y ./google-chrome-stable_current_amd64.deb

# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb



# RUN dpkg -i google-chrome-stable_current_amd64.deb
# RUN apt -f -y install
# RUN dpkg -i google-chrome-stable_current_amd64.deb

# create a folder
WORKDIR /usr/src/app
RUN git clone https://github.com/chemradio/cta-gfx-telegram-bot.git .
RUN git switch pre-docker
RUN pip install -r requirements.txt

COPY config_and_db /usr/src/app/config_and_db/

RUN python3 app.py