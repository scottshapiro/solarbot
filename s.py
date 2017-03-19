from app import getsolar, setsolar
import os
import time
from rq import Queue
from worker import conn

q = Queue('low', async=False, connection=conn)

job = q.enqueue(setsolar,os.environ["ENPHASE_KEY"],os.environ["ENPHASE_USER_ID"],os.environ["ENPHASE_SYSTEM_ID"])

print getsolar(os.environ["ENPHASE_KEY"],os.environ["ENPHASE_USER_ID"],os.environ["ENPHASE_SYSTEM_ID"])

