# FROM --platform=linux/amd64 python:3.9
FROM python:3.9

RUN apt update
RUN apt -y upgrade
RUN apt install -y ffmpeg

WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 9000
ENV IS_DOCKER yes

CMD [ "python3", "app.py" ]