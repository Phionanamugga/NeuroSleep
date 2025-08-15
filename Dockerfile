# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (ping, curl for health checks, and netcat)
RUN apt-get update && \
    apt-get install -y \
    iputils-ping \
    netcat-openbsd \
    curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements.txt to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy both backend and frontend code to the container
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Set working directory to backend for uvicorn
WORKDIR /app/backend

# Expose the port Uvicorn will run on
EXPOSE 8000

# Environment variables
ENV PYTHONPATH=/app
ENV UVICORN_RELOAD=true

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Command to run the FastAPI application with auto-reload in development
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

