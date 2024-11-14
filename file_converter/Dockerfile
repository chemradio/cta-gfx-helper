# FROM --platform=linux/amd64 python:3.9
FROM python:3.10

RUN apt update
RUN apt -y upgrade

RUN apt-get install -y build-essential libssl-dev libffi-dev
RUN apt-get install -y libreoffice

WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY . .

EXPOSE 9002

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9005", "--reload"]