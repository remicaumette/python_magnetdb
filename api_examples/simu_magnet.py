import os
import sys
import datetime
from datetime import timezone
from datetime import datetime

import requests

api_server = os.getenv('MAGNETDB_API_SERVER') or "http://magnetdb-api.grenoble.lncmi.local"
magnet_name = 'HL-test'

r = requests.get(
    f"{api_server}:8000/api/magnets",
    headers={'Authorization': os.getenv('MAGNETDB_API_KEY')}
)

for magnet in r.json()['items']:
    print(f"MAGNET: {magnet['name']} (status:{magnet['status']}, id:{magnet['id']})")
    if magnet['name'] == magnet_name:
        found = True
        break

if not found:
    sys.exit(1)

# Create a simu

sim_data={
    'resource_type': 'magnet',
    'resource_id': magnet['id'],
    'method': 'cfpdes',
    'model': 'thmagel_hcurl',
    'geometry': 'Axi',
    'cooling': 'meanH',
    'static': True,
    'non_linear': True
    }
   
print(sim_data)

ct = datetime.utcnow()
print(f"current time: {datetime.now()}")
print(f"current time (UTC): {datetime.utcnow()}")
# print(f"current time: {ct.replace(tzinfo=timezone.utc)}")

requests.post(
    f"{api_server}:8000/api/simulations",
    data=sim_data,
    headers={'Authorization': os.getenv('MAGNETDB_API_KEY')}
)

# how to get simu_id
r = requests.get(f"{api_server}:8000/api/simulations", headers={'Authorization': os.getenv('MAGNETDB_API_KEY')})
print(f"result: type={type(r.json()['items'])}")
result_list = r.json()['items']
simu = result_list[-1]
simu_id = simu['id']

# however shall check timestamp and author
print(f"simu_id={simu['id']}: create_at={simu['created_at']}, ct={ct}")
t1 = datetime.strptime(simu['created_at'], "%Y-%m-%dT%X.%f")
print(f"t1: {t1}")
diff = t1 - ct
print(f'tdiff: {diff} seconds: {diff.seconds}  milliseconds: {diff.microseconds/1000.}')    

# # how to get user name?
# from db result_list[-1]['owner']['name']:
    
# Run setup
r = requests.post(
    f"{api_server}:8000/api/simulations/{simu_id}/run_setup",
    headers={'Authorization': os.getenv('MAGNETDB_API_KEY')}
)

# Run simu with ssh
r = requests.get(f"{api_server}:8000/api/servers", headers={'Authorization': os.getenv('MAGNETDB_API_KEY')})
print(f"result: type={type(r.json()['items'])}")
result_list = r.json()['items']
for server in result_list:
    print(f'server: {server}')
    
# r = requests.post(
#     f"{api_server}:8000/api/simulations/{simu_id}/run?server_id={server_id}",
#     headers={'Authorization': os.getenv('MAGNETDB_API_KEY')}
# )
