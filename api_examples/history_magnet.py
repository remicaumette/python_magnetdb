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
magnet_name = 'M19061901'

for magnet_name in args.names:
    print(f'looking for: {magnet_name}')

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
            # list_records.append(record['id'])
            # temporary hack
            print(f'record: {record}')
            rname = record['name']
            actual_site = rname.split('_')[0]
            list_records.append(f"../../python_magnetrun/{rname}")
            # get record file from S3
            # print(f"record={rname}, actual_site={actual_site}")

