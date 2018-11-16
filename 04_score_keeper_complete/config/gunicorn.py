import os
from multiprocessing import cpu_count

bind = ['0.0.0.0:80']
workers = cpu_count() * 4
worker_class = 'gevent'
accesslog = '-'
errorlog = '-'

for k, v in os.environ.items():
    if k.startswith("GUNICORN_"):
        key = k.split('_', 1)[1].lower()
        locals()[key] = v
