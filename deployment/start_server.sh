#!/bin/bash

# Start Gunicorn server for PyGroove

cd /home/lar_mo/pygroove.lar-mo.com/pygroove
source ../venv/bin/activate

# Check if server is already running
if [ -f ../logs/gunicorn.pid ]; then
    PID=$(cat ../logs/gunicorn.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "Server is already running (PID: $PID)"
        exit 1
    fi
fi

echo "Starting Gunicorn server for PyGroove..."
nohup gunicorn \
    --config /home/lar_mo/pygroove.lar-mo.com/pygroove/deployment/gunicorn.conf.py \
    pygroove.wsgi:application \
    > /home/lar_mo/pygroove.lar-mo.com/logs/nohup.log 2>&1 &

sleep 2

if [ -f ../logs/gunicorn.pid ]; then
    echo "Server started successfully on port 8002"
    echo "PID: $(cat ../logs/gunicorn.pid)"
else
    echo "Failed to start server. Check logs:"
    echo "  tail -f ../logs/gunicorn_error.log"
    exit 1
fi
