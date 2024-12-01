FROM python:3.12

ARG PORT=9000
ENV PORT=$dispatcher_port

RUN apt update
RUN apt -y upgrade

WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
COPY libs /libs
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE $PORT

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000", "--reload", "--workers", "1"]

# CMD ["python3", "main.py"]
