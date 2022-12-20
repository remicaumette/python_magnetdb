import os
import sys
import datetime
from datetime import timezone
from datetime import datetime
from time import sleep

import requests

api_server = os.getenv('MAGNETDB_API_SERVER') or "http://magnetdb-api.grenoble.lncmi.local"
part_name = 'H15101601'
server_name = 'calcul22'

r = requests.get(
    f"{api_server}:8000/api/parts",
    headers={'Authorization': os.getenv('MAGNETDB_API_KEY')}
)

result_list = r.json()['items']
for part in result_list:
    print(f"PART: {part['name']} id:{part['id']})")
    if part['name'] == part_name:
        found = True
        break

if not found:
    print(f"part: {part_name} not found in magnetdb ({api_server})")
    print(f"available parts: {[part['name'] for part in result_list]}")
    sys.exit(1)

r = requests.get(
    f"{api_server}:8000/api/parts/{part['id']}",
    headers={'Authorization': os.getenv('MAGNETDB_API_KEY')}
)

# print(f'result={r.json()}, type={type(r.json())}')
list_records = []
data=r.json()
for magnet in data['magnet_parts']:
    # print(f"magnet={magnet}, id={magnet['magnet_id']}")
    magnet_result = requests.get(
        f"{api_server}:8000/api/magnets/{magnet['magnet_id']}",
        headers={'Authorization': os.getenv('MAGNETDB_API_KEY')}
    )

    magnet_data = magnet_result.json()
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

