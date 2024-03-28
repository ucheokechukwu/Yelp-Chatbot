#!/bin/bash

# Run any setup steps or preprocessing tasks here
echo "Starting Yelp RAG FASTAPI service..."

# Start the main application
uvicorn main:app --host 0.0.0.0 --port 8000