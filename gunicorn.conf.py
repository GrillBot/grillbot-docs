# Production server for the docs (see Dockerfile). Flask's built-in server is for development only.

bind = "0.0.0.0:80"

# The master binds port 80 as root, then the workers drop to an unprivileged user.
user = "nobody"
group = "nobody"

# One worker keeps memory inside the 128M Swarm limit and shares the in-process cache; the threads cover the
# blocking outbound requests (GitHub, health checks). Scale with replicas instead of workers.
worker_class = "gthread"
workers = 1
threads = 4
timeout = 30

# Heartbeat files on tmpfs, so a slow container filesystem cannot make the master think a worker is stuck.
worker_tmp_dir = "/dev/shm"

accesslog = "-"
errorlog = "-"
