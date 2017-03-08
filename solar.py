from urllib2 import Request, urlopen, URLError
import json

def solar():

    request = Request('https://api.enphaseenergy.com/api/v2/systems/45157/summary?key=3fbdaa7269e667f13a87d33c2b8d5e09&user_id=4f4449314e6a63350a')

    try:
        # response ='{"system_id":45157,"modules":14,"size_w":2660,"current_power":3,"energy_today":11491,"energy_lifetime":21668606,"summary_date":"2017-03-07","source":"microinverters","status":"normal","operational_at":1321406693,"last_report_at":1488939265,"last_interval_end_at":1488939052}'
	response = urlopen(request)
	solar = json.loads(response.read())
	message = str(solar['energy_today']) + "Wh were produced today.\n" + str(solar['current_power']) + "W this moment."
	print message
	return message
    except URLError, e:
        print 'No kittez. Got an error code:', e
