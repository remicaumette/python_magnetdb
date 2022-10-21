import os

import requests

r = requests.get("http://localhost:8000/api/magnets", headers={'Authorization': os.getenv('MAGNETDB_API_KEY')})
for magnet in r.json()['items']:
    print(f"MAGNET: {magnet['name']} ({magnet['status']})")
