FROM python:3.7-slim

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN apt-get -y install vim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY gunicorn.conf.py /code/gunicorn.conf.py

COPY alembic.ini /code/alembic.ini

COPY migrations /code/migrations

COPY .env.dev /code/.env.dev

