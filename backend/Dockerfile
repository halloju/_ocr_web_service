# Build stage
FROM python:3.9.5-alpine AS build

RUN apk --no-cache add libpq gcc vim poppler-utils && \
    apk --no-cache add --virtual .build-deps musl-dev postgresql-dev

WORKDIR /code

COPY ./requirements.txt .

RUN pip install -U pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

# Production stage
FROM python:3.9.5-alpine

RUN apk --no-cache add libpq poppler-utils

WORKDIR /usr/src/app

COPY --from=build /code /usr/src/app

COPY gunicorn.conf.py .

COPY .env.dev .

CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:app"]


