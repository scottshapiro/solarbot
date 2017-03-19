# setsolar.py
# script to call the function that pulls solar data from the Enphase API and store it in redis

from app import setsolar
import os
from rq import Queue
from worker import conn
import redis

r = redis.from_url(os.environ.get("REDIS_URL"))

setsolar(os.environ["ENPHASE_KEY"],os.environ["ENPHASE_USER_ID"],os.environ["ENPHASE_SYSTEM_ID"]) #set solar data in redis

