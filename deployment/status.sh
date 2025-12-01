#!/bin/bash

# Check status of PyGroove server

PIDFILE="/home/lar_mo/pygroove.lar-mo.com/logs/gunicorn.pid"

echo "=== PyGroove Server Status ==="
echo

if [ ! -f "$PIDFILE" ]; then
    echo "Status: NOT RUNNING (no PID file)"
    exit 1
fi

PID=$(cat "$PIDFILE")

if ps -p $PID > /dev/null 2>&1; then
    echo "Status: RUNNING"
    echo "PID: $PID"
    echo "Port: 8002"
    echo
    echo "Process info:"
    ps -p $PID -o pid,ppid,user,%cpu,%mem,etime,command
    echo
    echo "Recent access log (last 5 lines):"
    tail -5 /home/lar_mo/pygroove.lar-mo.com/logs/gunicorn_access.log 2>/dev/null || echo "No access log found"
else
    echo "Status: NOT RUNNING (stale PID file)"
    echo "Stale PID: $PID"
    rm -f "$PIDFILE"
    exit 1
fi
