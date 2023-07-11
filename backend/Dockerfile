# # Use an alias for the base image
# FROM python:3.9-slim

# # Set the working directory
# WORKDIR /code

# # Install required packages and build dependencies
# RUN apt-get update && apt-get -y install libpq-dev gcc libxml2-dev libxmlsec1-dev libxmlsec1-openssl && apt-get -y install vim && apt-get -y install poppler-utils && apt-get -y install poppler-data && apt-get -y install musl-dev

# # Copy the requirements file
# COPY ./requirements.txt .

# # Upgrade pip and install the required packages from the requirements file
# RUN pip install -U pip && \
#     pip install --no-cache-dir --upgrade -r requirements.txt

# # Copy the rest of the application code
# COPY . .

# Use an alias for the base image
FROM python:3.9-slim as base

# Set the working directory
WORKDIR /code

# Install required packages and build dependencies
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y \
    libpq-dev \
    libxslt-dev \
    python3-dev \
    build-essential \
    gcc \
    libxml2-dev \
    libxmlsec1-dev \
    libxmlsec1-openssl \
    vim \
    poppler-utils \
    poppler-data \
    musl-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY ./requirements.txt .

# Upgrade pip and install the required packages from the requirements file
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip uninstall lxml -y && \
    pip install --no-binary lxml lxml==4.9.1

# Copy the rest of the application code
COPY . .

# Use multi-stage build to reduce image size
FROM base as final
COPY --from=base /code /code
