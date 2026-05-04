#!/bin/bash

while true
do
  echo "Cleaning port 8087..."
  lsof -ti tcp:8087 | xargs kill -9 2>/dev/null

  sleep 2

  echo "Starting server..."
  python3.14 main.py &

  # Wait for 5 minutes (300 seconds)
  sleep 300

  echo "Restarting server..."
done