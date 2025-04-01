# Use a base image with Python
FROM python:3.12-slim

# Install FFmpeg for audio processing
RUN apt-get update && apt-get install -y ffmpeg
RUN apt-get update && apt-get install -y fs

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 8080

# Run the app
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8080"]