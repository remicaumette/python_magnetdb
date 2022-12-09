import os
import sys
import datetime
from datetime import timezone
from datetime import datetime
from time import sleep

import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("names", help="site names (ex. M9_M19061901)", nargs='+', metavar='SiteNames', type=str, default="M9_M19061901")
args = parser.parse_args()

print(f'args: {args}')

api_server = os.getenv('MAGNETDB_API_SERVER') or "http://magnetdb-api.grenoble.lncmi.local"

for _name in args.names:
    print(f'looking for: {_name}')
    
    r = requests.get(
        f"{api_server}:8000/api/sites",
        headers={'Authorization': os.getenv('MAGNETDB_API_KEY')}
    )

    found = False
    result_list = r.json()['items']
    for item in result_list:
        if item['name'] == _name:
            print(f"SITE: {item['name']} (status:{item['status']}, id:{item['id']})")
            found = True
            break

    if not found:
        print(f"site: {_name} not found in magnetdb ({api_server})")
        print(f"available sites: {[item['name'] for item in result_list]}")
        sys.exit(1)

    r = requests.get(
        f"{api_server}:8000/api/sites/{item['id']}",
        headers={'Authorization': os.getenv('MAGNETDB_API_KEY')}
    )

    _list = []
    _data = r.json()
    # for key in _data:
    #     print(key)
    # print(f"data[{_name}]: records={len(_data['records'])}")
    
    # print(f"data[{_name}]: site_magnets={_data['site_magnets']}")
    for magnet in _data['site_magnets']:
        # print(f"magnet={magnet}, id={magnet['magnet_id']}")
        _result = requests.get(
            f"{api_server}:8000/api/magnets/{magnet['magnet_id']}",
            headers={'Authorization': os.getenv('MAGNETDB_API_KEY')}
        )
        magnet_data = _result.json()
        _list.append(magnet_data['name'])
        # print(f"magnet: {magnet_data['name']}")
    print(f'magnets: {_list}')
    
    

