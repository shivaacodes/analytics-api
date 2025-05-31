#!/bin/bash

# Activate the virtual environment
source /opt/venv/bin/activate

# Move to app directory
cd /app

# Set runtime variables
RUN_PORT=${PORT:-8000}
RUN_HOST=${HOST:-0.0.0.0}

# Start the FastAPI app with Gunicorn + Uvicorn worker
gunicorn -k uvicorn.workers.UvicornWorker -b $RUN_HOST:$RUN_PORT main:app
