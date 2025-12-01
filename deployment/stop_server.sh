#!/bin/bash

# Stop Gunicorn server for PyGroove

PIDFILE="/home/lar_mo/pygroove.lar-mo.com/logs/gunicorn.pid"

if [ ! -f "$PIDFILE" ]; then
    echo "Server is not running (no PID file found)"
    exit 1
fi

PID=$(cat "$PIDFILE")

if ! ps -p $PID > /dev/null 2>&1; then
    echo "Server is not running (stale PID file)"
    rm -f "$PIDFILE"
    exit 1
fi

echo "Stopping PyGroove server (PID: $PID)..."
kill $PID

# Wait for graceful shutdown
for i in {1..10}; do
    if ! ps -p $PID > /dev/null 2>&1; then
        rm -f "$PIDFILE"
        echo "Server stopped successfully"
        exit 0
    fi
    sleep 1
done

# Force kill if still running
if ps -p $PID > /dev/null 2>&1; then
    echo "Forcing server shutdown..."
    kill -9 $PID
    rm -f "$PIDFILE"
    echo "Server forcefully stopped"
fi
