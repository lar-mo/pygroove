# PyGroove Deployment Guide - Dreamhost VPS

Complete guide for deploying PyGroove to Dreamhost VPS.

## Quick Reference

- **Domain**: pygroove.lar-mo.com
- **Port**: 8002
- **VPS Path**: `/home/lar_mo/pygroove.lar-mo.com/`
- **SSH Alias**: `dhvps` (configured in `~/.ssh/config`)
- **Python**: 3.10.12

## Prerequisites

- Dreamhost VPS account
- SSH access configured (alias: `dhvps`)
- Subdomain `pygroove.lar-mo.com` created in Dreamhost panel

## Deployment Steps

### 1. Upload Project to VPS

From your local machine:

```bash
cd /Users/larrymoiola/Code/GitHub/pygroove
rsync -avz --exclude='venv' --exclude='*.pyc' --exclude='__pycache__' \
  --exclude='db.sqlite3' --exclude='media' --exclude='.git' --exclude='secrets.json' \
  . dhvps:/home/lar_mo/pygroove.lar-mo.com/pygroove/
```

### 2. SSH into VPS

```bash
ssh dhvps
cd /home/lar_mo/pygroove.lar-mo.com
```

### 3. Create Directory Structure

```bash
mkdir -p logs
```

### 4. Set Up Virtual Environment

```bash
virtualenv -p python3 venv
source venv/bin/activate
pip install --upgrade pip
cd pygroove
pip install -r requirements.txt
```

### 5. Create Production secrets.json

```bash
cd /home/lar_mo/pygroove.lar-mo.com/pygroove
cp deployment/secrets.json.template secrets.json
nano secrets.json
```

Update with production values:
```json
{
  "SECRET_KEY": "your-new-production-secret-key",
  "DISCOGS_TOKEN": "your-discogs-token",
  "COLLECTOR_EMAIL": "phpcds@aretemm.net",
  "EMAIL_HOST_USER": "",
  "EMAIL_HOST_PASSWORD": "",
  "ALLOWED_HOSTS": ["pygroove.lar-mo.com", "localhost", "127.0.0.1"],
  "DEBUG": false
}
```

Generate new SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Upload Media Files (if needed)

If you have existing album covers and artist images, upload them from local machine:

```bash
rsync -avz /Users/larrymoiola/Code/GitHub/pygroove/media/ \
  dhvps:/home/lar_mo/pygroove.lar-mo.com/pygroove/media/
```

### 7. Collect Static Files

```bash
cd /home/lar_mo/pygroove.lar-mo.com/pygroove
source ../venv/bin/activate
python manage.py collectstatic --noinput
```

### 8. Run Migrations

```bash
python manage.py migrate
```

### 9. Make Scripts Executable

```bash
chmod +x deployment/*.sh
```

### 10. Set Up Systemd with Linger (Auto-restart)

```bash
cd /home/lar_mo/pygroove.lar-mo.com/pygroove
./deployment/setup_linger.sh
```

This enables:
- Auto-start on VPS reboot
- Service management via systemd

### 11. Start the Server

**Option A: Using systemd (recommended)**
```bash
systemctl --user start pygroove
systemctl --user status pygroove
```

**Option B: Using start script**
```bash
./deployment/start_server.sh
```

### 12. Verify Server is Running

```bash
./deployment/status.sh
```

Or test locally on VPS:
```bash
curl http://localhost:8002/
```

### 13. Configure Dreamhost Proxy Server

**CRITICAL STEP!** This connects your domain to the running application.

1. Log into [Dreamhost Panel](https://panel.dreamhost.com)
2. Navigate to: **Servers → VPS → Proxy Server**
3. Click **"Add Proxy Server"**
4. Fill in:
   - **Domain**: `pygroove.lar-mo.com`
   - **Port**: `8002`
5. Click **"Add Proxy Now"**
6. Wait 5-15 minutes for "Installing..." to change to "Active"

### 14. Test Live Site

```bash
curl https://pygroove.lar-mo.com/
```

Or visit in browser: https://pygroove.lar-mo.com

## Server Management

### Start Server
```bash
systemctl --user start pygroove
# or
./deployment/start_server.sh
```

### Stop Server
```bash
systemctl --user stop pygroove
# or
./deployment/stop_server.sh
```

### Restart Server
```bash
systemctl --user restart pygroove
# or
./deployment/restart_server.sh
```

### Check Status
```bash
systemctl --user status pygroove
# or
./deployment/status.sh
```

### View Logs
```bash
# Systemd logs
journalctl --user -u pygroove -f

# Gunicorn logs
tail -f ~/pygroove.lar-mo.com/logs/gunicorn_error.log
tail -f ~/pygroove.lar-mo.com/logs/gunicorn_access.log
```

## Updating Code

When you push changes to GitHub, SSH into VPS and pull the updates:

```bash
ssh dhvps
cd /home/lar_mo/pygroove.lar-mo.com/pygroove

# Pull latest changes
git pull origin main

# Activate venv
source ../venv/bin/activate

# Install any new dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Restart server
systemctl --user restart pygroove
```

## Troubleshooting

### Server won't start
```bash
# Check logs
tail -20 ~/pygroove.lar-mo.com/logs/gunicorn_error.log

# Check if port is in use
lsof -i :8002

# Verify secrets.json exists and is valid
cat secrets.json
```

### 502/404 errors on domain
```bash
# Verify Gunicorn is running
./deployment/status.sh

# Check Dreamhost Proxy is Active
# Go to Panel → Servers → VPS → Proxy Server
# Should show "Active" not "Installing"
```

### ALLOWED_HOSTS error
```bash
# Edit secrets.json
nano secrets.json

# Add your domain to ALLOWED_HOSTS
"ALLOWED_HOSTS": ["pygroove.lar-mo.com", "localhost", "127.0.0.1"]

# Restart
systemctl --user restart pygroove
```

### Static files not loading
```bash
# Recollect static files
python manage.py collectstatic --noinput --clear

# Restart server
systemctl --user restart pygroove
```

## SSL Certificate

Dreamhost automatically provides SSL. If not working:

1. Go to **Websites → Manage Websites**
2. Find `pygroove.lar-mo.com`
3. Click **"Manage"**
4. Enable **"Let's Encrypt SSL"**

## Important Files

- `deployment/gunicorn.conf.py` - Gunicorn configuration
- `deployment/pygroove.service` - Systemd service file
- `deployment/*.sh` - Management scripts
- `secrets.json` - Production secrets (NOT in git)
- `logs/` - Server logs

## Checklist

- [ ] Upload project to VPS
- [ ] Create virtualenv and install dependencies
- [ ] Create production `secrets.json`
- [ ] Upload media files (album covers)
- [ ] Collect static files
- [ ] Run migrations
- [ ] Make scripts executable
- [ ] Set up systemd with Linger
- [ ] Start Gunicorn server
- [ ] Configure Dreamhost Proxy Server
- [ ] Wait for proxy installation (5-15 min)
- [ ] Test domain access
- [ ] Verify SSL certificate

## Support

For issues, check:
1. Gunicorn error logs: `~/pygroove.lar-mo.com/logs/gunicorn_error.log`
2. Systemd status: `systemctl --user status pygroove`
3. Dreamhost proxy status: Panel → Servers → VPS → Proxy Server
