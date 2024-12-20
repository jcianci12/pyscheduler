FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Set working directory

# Run server.py when the container starts
CMD ["python3", "server.py"]
