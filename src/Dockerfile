# Use the official Python image as the base image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy the application files into the container
COPY . .

# Install system dependencies required for dbus-python and other packages
RUN apt-get update && apt-get install -y \
    pkg-config \
    libdbus-1-dev \
    libssl-dev \
    gcc \
    python3-apt \
    python3-dev \
    gobject-introspection \
    libgirepository1.0-dev \
    libsystemd-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip before installing dependencies
RUN pip install --upgrade pip

# Install required Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the script when the container starts
CMD ["python", "app.py"]

