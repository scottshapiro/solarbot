from app import solar
import os
import time
from rq import Queue
from worker import conn

q = Queue('low', async=False, connection=conn)

job = q.enqueue(solar,os.environ["ENPHASE_KEY"],os.environ["ENPHASE_USER_ID"],os.environ["ENPHASE_SYSTEM_ID"])
print job.result

