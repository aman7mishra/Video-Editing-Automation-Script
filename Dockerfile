# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install the necessary dependencies for a Windows container
RUN apt-get update && apt-get install -y \
    imagemagick \
    gcc \
    espeak \
    portaudio19-dev \
    python3-pyaudio \
    ffmpeg \
    libsm6 \
    libxext6 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the custom policy.xml into the correct location
COPY ./utils/policy.xml /etc/ImageMagick-6/policy.xml

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure the media_files directory has the correct permissions (for Windows, chmod can be skipped)
# This line is optional depending on your file permissions setup
RUN chmod -R 755 /usr/src/app/media_files || echo "Skipping chmod on Windows"

# Run the script
CMD ["python", "./src/script.py"]
