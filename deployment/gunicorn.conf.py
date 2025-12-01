import multiprocessing

# Server socket
bind = "0.0.0.0:8002"

# Worker processes
workers = 2  # Use 2+ workers (PyGroove doesn't self-call, but 2 is good practice)
worker_class = "sync"
timeout = 30
keepalive = 2

# Logging
accesslog = "/home/lar_mo/pygroove.lar-mo.com/logs/gunicorn_access.log"
errorlog = "/home/lar_mo/pygroove.lar-mo.com/logs/gunicorn_error.log"
loglevel = "info"

# Process naming
proc_name = "pygroove"

# PID file
pidfile = "/home/lar_mo/pygroove.lar-mo.com/logs/gunicorn.pid"
