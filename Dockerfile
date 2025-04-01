# Use a base image with Python
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-2.0-0 \
    && apt-get clean

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install necessary PostgreSQL development libraries
RUN apt-get update && apt-get install -y libpq-dev

# Add ASLA virtual audio device
RUN apt-get update && apt-get install -y alsa-utils

# Configure ASLA
RUN echo "pcm.!default { type hw card 0 }" > /etc/asound.conf
RUN echo "ctl.!default { type hw card 0 }" >> /etc/asound.conf

# Expose the port
EXPOSE 8080

# Run the app
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8080"]