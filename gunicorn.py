import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
bind = '127.0.0.1:5000'
backlog = 2048
worker_class = "sync"
debug = True
proc_name = 'gunicorn.proc'
pidfile = '/tmp/gunicorn.pid'
logfile = '/var/log/gunicorn/debug.log'
loglevel = 'debug'
