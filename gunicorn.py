import multiprocessing

bind = '0.0.0.0:5000'
# 开启进程
workers = 1
# workers = multiprocessing.cpu_count()

# 每个进程的开启线程
threads = 5

# debug=True
# 如果不使用supervisord之类的进程管理工具需要设置为守护进程，否则会出问题
daemon = True

# 进程名称
proc_name = 'gunicorn.pid'
# 进程pid记录文件
pidfile = '/var/log/gunicorn/app_pid.log'
loglevel = 'debug'
logfile = '/var/log/gunicorn/debug.log'
accesslog = '/var/log/gunicorn/access.log'
access_log_format = '%(h)s %(t)s %(U)s %(q)s'
