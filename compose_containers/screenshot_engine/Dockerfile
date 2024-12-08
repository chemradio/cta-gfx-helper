FROM python:3.12

RUN apt update
RUN apt -y upgrade

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY libs libs
RUN pip install --no-cache-dir ./libs/py_gfxhelper_lib

COPY . .

EXPOSE 9002

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9002", "--reload", "--workers", "1"]