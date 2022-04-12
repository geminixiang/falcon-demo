import gevent.monkey
import multiprocessing


gevent.monkey.patch_all()

daemon = True
bind = '0.0.0.0:8000'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'
backlog = 2048
keepalive = 5
