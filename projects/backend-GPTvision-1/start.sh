#!/bin/bash
# Start script for Render deployment

# Use gunicorn with uvicorn workers for production
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT 