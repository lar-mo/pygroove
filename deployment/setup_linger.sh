#!/bin/bash

# Setup systemd user service with Linger for PyGroove
# Run this once on the VPS to enable auto-start on reboot

echo "=== Setting up PyGroove systemd service ==="
echo

# Create user systemd directory
mkdir -p ~/.config/systemd/user

# Copy service file
cp /home/lar_mo/pygroove.lar-mo.com/pygroove/deployment/pygroove.service ~/.config/systemd/user/

# Enable linger (allows user services to run without login)
loginctl enable-linger $USER

# Reload systemd
systemctl --user daemon-reload

# Enable the service
systemctl --user enable pygroove.service

echo
echo "✓ Linger enabled for user: $USER"
echo "✓ Service installed: pygroove.service"
echo "✓ Service will auto-start on reboot"
echo
echo "Commands:"
echo "  Start:   systemctl --user start pygroove"
echo "  Stop:    systemctl --user stop pygroove"
echo "  Restart: systemctl --user restart pygroove"
echo "  Status:  systemctl --user status pygroove"
echo "  Logs:    journalctl --user -u pygroove -f"
