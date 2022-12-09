import os

import requests

api_server = os.getenv('MAGNETDB_API_SERVER') or "http://magnetdb-api.grenoble.lncmi.local"

r = requests.get(f"{api_server}:8000/api/sites", headers={'Authorization': os.getenv('MAGNETDB_API_KEY')})
for magnet in r.json()['items']:
    print(f"SITE: {magnet['name']} (status:{magnet['status']}, id:{magnet['id']})")
