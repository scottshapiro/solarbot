import os
import sys
import json
import redis
from urllib2 import Request, urlopen, URLError

import requests
from flask import Flask, request

from rq import Queue
# from worker import conn

app = Flask(__name__)


# q = Queue(connection=conn)
r = redis.from_url(os.environ.get("REDIS_URL"))

def setsolar(key,user_id,system_id):
    try:
        request = Request('https://api.enphaseenergy.com/api/v2/systems/'+system_id+'/summary?key='+key+'&user_id='+user_id)
        response = urlopen(request)
        solar = json.loads(response.read())
	r.hset(user_id,'energy_today',solar['energy_today'])
	r.hset(user_id,'current_power',solar['current_power'])
    except URLError, e:
        print 'No kittez. Got an error code:', e

def getsolar(key,user_id,system_id):
        message = str(r.hget(user_id,'energy_today')) + "Wh were produced today. " + str(r.hget(user_id,'current_power')) + "W this moment."
        return message


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return 'verified', 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
		    r.hset(os.environ["ENPHASE_USER_ID"],'sender_id',sender_id)

                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
		    r.hset(os.environ["ENPHASE_USER_ID"],'recipient_id',recipient_id)

                    # job = q.enqueue(setsolar,os.environ["ENPHASE_KEY"],os.environ["ENPHASE_USER_ID"],os.environ["ENPHASE_SYSTEM_ID"]) #set solar data in redis

		    #log(job)

 		    report = getsolar(os.environ["ENPHASE_KEY"],os.environ["ENPHASE_USER_ID"],os.environ["ENPHASE_SYSTEM_ID"]) #pull solar data from redis

                    send_message(sender_id, "Instant report: " + report)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200

def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
