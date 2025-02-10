# Use the official Python image as the base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy application files into the container
COPY . .

# Install system dependencies required for dbus-python and other packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    pkg-config \
    libdbus-1-dev \
    libssl-dev \
    gcc \
    python3-apt \
    python3-dev \
    gobject-introspection \
    libgirepository1.0-dev \
    libsystemd-dev \
    libdbus-glib-1-dev \
    dbus \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip before installing dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Set an environment variable for the S3 bucket (override during runtime if needed)
ENV BUCKET_NAME="default-bucket-name"

# Create a non-root user and switch to it for security
RUN useradd -m appuser
USER appuser

# Command to run the script when the container starts
CMD ["python", "app.py"]
