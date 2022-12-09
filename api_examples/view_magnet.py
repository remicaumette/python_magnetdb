import os
import sys
import datetime
from datetime import timezone
from datetime import datetime
from time import sleep

import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("names", help="magnet names (ex. M19061901)", nargs='+', metavar='MagnetNames', type=str, default="M19061901")
args = parser.parse_args()

print(f'args: {args}')

api_server = os.getenv('MAGNETDB_API_SERVER') or "http://magnetdb-api.grenoble.lncmi.local"

for magnet_name in args.names:
    print(f'looking for: {magnet_name}')
    
    r = requests.get(
        f"{api_server}:8000/api/magnets",
        headers={'Authorization': os.getenv('MAGNETDB_API_KEY')}
    )

    found = False
    result_list = r.json()['items']
    for magnet in result_list:
        if magnet['name'] == magnet_name:
            print(f"MAGNET: {magnet['name']} (status:{magnet['status']}, id:{magnet['id']})")
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

    _list = []
    magnet_data = r.json()
    for site in magnet_data['site_magnets']:
        # print(f"site={site}, id={site['site_id']}")
        site_result = requests.get(
            f"{api_server}:8000/api/sites/{site['site_id']}",
            headers={'Authorization': os.getenv('MAGNETDB_API_KEY')}
        )
        site_data = site_result.json()
        _list.append(site_data['name'])
        # print(f"site: {site_data['name']}")
    print(f'sites: {_list}')
    
    _list = []
    for part in magnet_data['magnet_parts']:
        # print(f"part={part}, id={part['part_id']}")
        part_result = requests.get(
            f"{api_server}:8000/api/parts/{part['part_id']}",
            headers={'Authorization': os.getenv('MAGNETDB_API_KEY')}
        )
        part_data = part_result.json()
        _list.append(part_data['name'])
        # print(f"part: {part_data['name']}")
    print(f'parts: {_list}')
    

