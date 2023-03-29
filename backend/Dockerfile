FROM python:3.9.5-slim-buster
RUN apt-get update \
    && apt-get -y install libpq-dev gcc vim poppler-utils

ARG MLAAS_XClient
ARG MLAAS_JWT
ARG MLAAS_URL=http://mlaas:7777

# set work directory
WORKDIR /usr/src/app

COPY ./requirements.txt /code/requirements.txt
RUN pip install -U pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

COPY gunicorn.conf.py /code/gunicorn.conf.py

COPY .env.dev /code/.env.dev

ENV MLAAS_XClient ${MLAAS_XClient}
ENV MLAAS_JWT ${MLAAS_JWT}
ENV MLAAS_URL ${MLAAS_URL}
