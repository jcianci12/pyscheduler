FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# Install dependencies
COPY requirements.txt .
RUN pip3 install --user -r requirements.txt

# Set working directory
WORKDIR /app