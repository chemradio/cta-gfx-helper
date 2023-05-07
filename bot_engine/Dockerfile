# FROM --platform=linux/amd64 python:3.9
FROM python:3.10

ARG PORT=9001
ENV PORT=$telegram_bot_port

RUN apt update
RUN apt -y upgrade
RUN apt -y install ffmpeg

WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE $PORT

CMD [ "python3", "main.py" ]