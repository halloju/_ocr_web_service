FROM python:3.9.5-slim-buster
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN apt-get -y install vim

# set work directory
WORKDIR /usr/src/app

COPY ./requirements.txt /code/requirements.txt
RUN pip install -U pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

COPY gunicorn.conf.py /code/gunicorn.conf.py

COPY .env.dev /code/.env.dev

