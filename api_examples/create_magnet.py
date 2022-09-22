import os

import requests

r = requests.post(
    "http://localhost:8000/api/magnets",
    data={'name': input('Magnet name? ')},
    headers={'Authorization': os.getenv('MAGNETDB_API_KEY')}
)

data = r.json()
if r.status_code != 200:
    print(data['detail'])
else:
    print(f"MAGNET: {data['name']} ({data['status']})")
