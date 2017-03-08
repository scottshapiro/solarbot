from urllib2 import Request, urlopen, URLError

def solar():

    request = Request('https://api.enphaseenergy.com/api/v2/systems/45157/summary?key=3fbdaa7269e667f13a87d33c2b8d5e09&user_id=4f4449314e6a63350a')

    try:
	response = urlopen(request)
	solar = response.read()
	print solar
    except URLError, e:
        print 'No kittez. Got an error code:', e
