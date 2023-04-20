# FROM --platform=linux/amd64 python:3.9
FROM python:3.10

ARG REBUILD_DB=false
ENV REBUILD_DB=$REBUILD_DB


RUN apt update
RUN apt -y upgrade

WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 9000
ENV IS_DOCKER yes


CMD ["python3", "main.py"]

# RUN if [ "$REBUILD_DB" = "true" ] ; then python3 rebuild_db.py ; fi
# CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "9000"]