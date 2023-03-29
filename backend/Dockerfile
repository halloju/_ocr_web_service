FROM python:3.9.5-alpine AS build

RUN apk --no-cache add libpq gcc vim poppler-utils && \
    apk --no-cache add --virtual .build-deps musl-dev

WORKDIR /code

COPY ./requirements.txt .

RUN pip install -U pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

