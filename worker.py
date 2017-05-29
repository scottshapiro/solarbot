import os
import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

# redis_url = os.getenv('REDISTOGO_URL', os.environ["REDISTOGO_URL"])

conn = redis.from_url(os.environ["REDISTOGO_URL"])

if __name__ == '__main__':
    with Connection(conn):
	print 'starting worker'
        worker = Worker(map(Queue, listen))
        worker.work()
