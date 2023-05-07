# FROM --platform=linux/amd64 python:3.9
FROM python:3.10

ARG PORT=9004
ENV PORT=$video_gfx_port

RUN apt update
RUN apt -y upgrade
RUN apt -y install ffmpeg

WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE $PORT

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "9004"]