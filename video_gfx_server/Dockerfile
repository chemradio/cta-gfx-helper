# FROM --platform=linux/amd64 python:3.9
FROM python:3.10

RUN apt update
RUN apt -y upgrade

WORKDIR /usr/src/app
# COPY requirements.txt requirements.txt
# RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 9006
ENV IS_DOCKER yes

CMD [ "python3", "main.py" ]