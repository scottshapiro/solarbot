import requests, json
url = 'https://api.enphaseenergy.com/api/v2/systems/?key=3fbdaa7269e667f13a87d33c2b8d5e09&user_id=4f4449314e6a63350a'
payload = json.load(open("request.json"))
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
r = requests.post(url, data=json.dumps(payload), headers=headers)
print r.getvalue()
