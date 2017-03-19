from urllib2 import Request, urlopen, URLError
import os
import json

def solar(key,user_id):

    request = Request('https://api.enphaseenergy.com/api/v2/systems/45157/summary?key='+key+'&user_id='+user_id)
    print request

    try:
	response = urlopen(request)
	solar = json.loads(response.read())
	message = str(solar['energy_today']) + "Wh were produced today.\n" + str(solar['current_power']) + "W this moment."
	return message
    except URLError, e:
        print 'No kittez. Got an error code:', e
