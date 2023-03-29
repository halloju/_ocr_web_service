# Use an alias for the base image
FROM python:3.9.5-alpine

# Set the working directory
WORKDIR /code

# Install required packages and build dependencies
RUN apk --no-cache add libpq gcc vim poppler-utils musl-dev

# Copy the requirements file
COPY ./requirements.txt .

# Upgrade pip and install the required packages from the requirements file
RUN pip install -U pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application code
COPY . .

# Declare build-time variables with default values
ARG MLAAS_XClient
ARG MLAAS_JWT
ARG MLAAS_URL=http://mlaas:7777

# Set environment variables using the ARG values
ENV MLAAS_XClient=${MLAAS_XClient} \
    MLAAS_JWT=${MLAAS_JWT} \
    MLAAS_URL=${MLAAS_URL}