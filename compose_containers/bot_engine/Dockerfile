FROM python:3.12

ARG PORT=9001

RUN apt update
RUN apt -y upgrade

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY libs libs
RUN pip install --no-cache-dir ./libs/py_gfxhelper_lib

COPY . .

EXPOSE $PORT

CMD [ "python3", "main.py" ]