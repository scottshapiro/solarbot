from app import send_message, getsolar, setsolar
import os
from rq import Queue
from worker import conn
import redis

r = redis.from_url(os.environ.get("REDIS_URL"))

send_message(r.hget(os.environ["ENPHASE_USER_ID"],'sender_id'),"Daily update: "+getsolar(os.environ["ENPHASE_KEY"],os.environ["ENPHASE_USER_ID"],os.environ["ENPHASE_SYSTEM_ID"]))
