# FROM --platform=linux/amd64 python:3.9
FROM python:3.12

RUN apt update
RUN apt -y upgrade

RUN apt-get install -y build-essential libssl-dev libffi-dev
RUN apt-get install -y libreoffice
RUN apt-get install -y ffmpeg

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
COPY libs libs
RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY . .

EXPOSE 9005

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9005"]