import os
import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDISTOGO_URL', 'redis://redistogo:cdc98dc1d537aa1bbb8df876e45836f9@koi.redistogo.com:11883/')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
	print 'starting worker'
        worker = Worker(map(Queue, listen))
        worker.work()
