#!/bin/bash

# Restart Gunicorn server for PyGroove

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Restarting PyGroove server..."

# Stop the server
"$SCRIPT_DIR/stop_server.sh"

# Wait a moment
sleep 2

# Start the server
"$SCRIPT_DIR/start_server.sh"
