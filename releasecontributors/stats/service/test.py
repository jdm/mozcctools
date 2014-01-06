import requests
import json


headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
data = {'product': 'Firefox'}
response = requests.get('http://127.0.0.1:5000/getActivityForProduct',
                        data=json.dumps(data),
                        headers=headers)
print response.status_code
print response.text

