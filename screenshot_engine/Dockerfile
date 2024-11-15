# FROM --platform=linux/amd64 python:3.9
FROM python:3.10

RUN apt update
RUN apt -y upgrade

WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 9002

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9002", "--reload", "--workers", "1"]