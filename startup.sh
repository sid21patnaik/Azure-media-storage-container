#!/bin/bash

# Ensure PORT is set by Azure
PORT=${PORT:-8000}

echo "Starting Gunicorn on port $PORT..."
exec gunicorn --bind=0.0.0.0:$PORT --timeout 600 run:app
