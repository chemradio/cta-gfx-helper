FROM python:3.10

ARG PORT=9000
ENV PORT=$dispatcher_port

RUN apt update
RUN apt -y upgrade

WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE $PORT

CMD ["python3", "main.py"]
