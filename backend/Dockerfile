# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV IS_DOCKER=true

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
# libgomp1 is required for some ML libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and download script
COPY requirements.txt download_models.py /app/

# Install CPU-only PyTorch first (Critical for Render Free Tier)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Install python dependencies from requirements
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the ML models
RUN python download_models.py

# Copy the rest of the application code
COPY . /app/

# Make port available (documentation only)
EXPOSE 8000

# Run the application using Gunicorn with Uvicorn workers
# We use the PORT environment variable which Render sets automatically
CMD sh -c "gunicorn -w 1 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:${PORT:-10000} --timeout 120"
