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

# Expose the port
EXPOSE 8080

# Run the app
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8080"]