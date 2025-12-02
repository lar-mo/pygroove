#!/bin/bash
#
# Download PyGroove database backup from production to local machine
# Usage: ./download_backup.sh
#

LOCAL_BACKUP_DIR="$HOME/backups/pygroove"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="pygroove_local_$TIMESTAMP.db"

# Create local backup directory
mkdir -p "$LOCAL_BACKUP_DIR"

echo "Downloading latest PyGroove database from production..."

# Download the database using SQLite backup command via SSH
ssh dhvps "sqlite3 /home/lar_mo/pygroove.lar-mo.com/pygroove/db.sqlite3 '.backup /tmp/pygroove_temp.db'" && \
scp dhvps:/tmp/pygroove_temp.db "$LOCAL_BACKUP_DIR/$BACKUP_FILE" && \
ssh dhvps "rm /tmp/pygroove_temp.db"

if [ $? -eq 0 ]; then
    BACKUP_SIZE=$(du -h "$LOCAL_BACKUP_DIR/$BACKUP_FILE" | cut -f1)
    echo "✓ Success! Backup downloaded ($BACKUP_SIZE)"
    echo "  Location: $LOCAL_BACKUP_DIR/$BACKUP_FILE"
    
    # List recent backups
    echo ""
    echo "Recent local backups:"
    ls -lht "$LOCAL_BACKUP_DIR" | head -6
else
    echo "✗ Backup failed"
    exit 1
fi
