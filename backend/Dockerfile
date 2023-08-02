# Use an alias for the base image
FROM python:3.10.12-slim as build

# Set the working directory
WORKDIR /code

# Install required packages and build dependencies
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y \
    libxslt-dev \
    python3-dev \
    build-essential \
    gcc \
    libxml2-dev \
    libxmlsec1-dev \
    libxmlsec1-openssl \
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

# Copy saml2 settings
COPY saml/uat/settings.json /code/app/static/saml/settings.json
RUN rm -rf saml/

# Start the runtime stage
FROM python:3.10.12-slim as final

WORKDIR /code

# Copy the built application from the build stage
COPY --from=build /code /code
COPY --from=build /usr/local /usr/local
COPY --from=build /usr/lib/x86_64-linux-gnu /usr/lib/x86_64-linux-gnu
RUN apt-get purge -y --allow-remove-essential \
    linux-libc-dev \
    perl-base
