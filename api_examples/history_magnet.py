import os
import sys
import datetime
from datetime import timezone
from datetime import datetime
from time import sleep

import requests

api_server = os.getenv('MAGNETDB_API_SERVER') or "http://magnetdb-api.grenoble.lncmi.local"
magnet_name = 'HL-test'
server_name = 'calcul22'

r = requests.get(
    f"{api_server}:8000/api/magnets",
    headers={'Authorization': os.getenv('MAGNETDB_API_KEY')}
)

result_list = r.json()['items']
for magnet in result_list:
    print(f"MAGNET: {magnet['name']} (status:{magnet['status']}, id:{magnet['id']})")
    if magnet['name'] == magnet_name:
        found = True
        break

if not found:
    print(f"magnet: {magnet_name} not found in magnetdb ({api_server})")
    print(f"available magnets: {[magnet['name'] for magnet in result_list]}")
    sys.exit(1)

r = requests.get(
    f"{api_server}:8000/api/magnets/{magnet['id']}",
    headers={'Authorization': os.getenv('MAGNETDB_API_KEY')}
)

# print(f'result={r.json()}, type={type(r.json())}')
list_records = []
magnet_data = r.json()
for site in magnet_data['site_magnets']:
    # print(f"site={site}, id={site['site_id']}")
    site_result = requests.get(
        f"{api_server}:8000/api/sites/{site['site_id']}",
        headers={'Authorization': os.getenv('MAGNETDB_API_KEY')}
    )
    site_data = site_result.json()
    #print(f'site_data={r.json()}, type={type(r.json())}')
    
    print(f"site={site_data['name']}, status={site_data['status']}, records:")
    for record in site_data['records']:
        list_records.append(record['id'])
        print(f"record={record['name']}")

