# PyGroove Database Backup System

## Overview
PyGroove uses a hybrid backup approach with automated weekly backups on the server and manual monthly off-site backups.

## Automated Server Backups

**Schedule:** Every Sunday at 2 AM  
**Retention:** Last 30 days  
**Location:** `/home/lar_mo/backups/pygroove/`

### Files
- **Script:** `/home/lar_mo/backup_pygroove.sh`
- **Log:** `/home/lar_mo/backups/pygroove_backup.log`

### Check Backup Status
```bash
ssh dhvps "cat /home/lar_mo/backups/pygroove_backup.log | tail -20"
```

### List Backups
```bash
ssh dhvps "ls -lh /home/lar_mo/backups/pygroove/"
```

### Manual Backup
```bash
ssh dhvps "/home/lar_mo/backup_pygroove.sh"
```

## Off-Site Backups (Monthly)

Download a backup to your local machine for off-site storage.

### Download Backup
```bash
cd ~/Code/GitHub/pygroove/deployment
./download_backup.sh
```

This downloads to: `~/backups/pygroove/`

## Restore from Backup

### Restore on Production
```bash
# Stop the server
ssh dhvps "cd /home/lar_mo/pygroove.lar-mo.com/pygroove/deployment && ./stop_server.sh"

# Restore database
ssh dhvps "cp /home/lar_mo/backups/pygroove/pygroove_YYYYMMDD_HHMMSS.db /home/lar_mo/pygroove.lar-mo.com/pygroove/db.sqlite3"

# Restart server
ssh dhvps "cd /home/lar_mo/pygroove.lar-mo.com/pygroove/deployment && ./start_server.sh"
```

### Restore on Local Development
```bash
cp ~/backups/pygroove/pygroove_local_YYYYMMDD_HHMMSS.db ~/Code/GitHub/pygroove/db.sqlite3
```

## Best Practices

1. **Weekly:** Automated backups run every Sunday
2. **Monthly:** Download off-site backup (first Sunday of month)
3. **Before major changes:** Run manual backup
4. **Test restores:** Periodically test restore process

## Backup Before Deployment
```bash
# Always backup before deploying major changes
ssh dhvps "/home/lar_mo/backup_pygroove.sh"
```
