# Use an alias for the base image
FROM python:3.9.5-alpine

# Set the working directory
WORKDIR /code

# Install required packages and build dependencies
RUN apk --no-cache add libpq gcc vim poppler-utils poppler-data musl-dev

# Copy the requirements file
COPY ./requirements.txt .

# Upgrade pip and install the required packages from the requirements file
RUN pip install -U pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application code
COPY . .

