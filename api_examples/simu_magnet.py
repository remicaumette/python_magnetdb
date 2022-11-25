import os
import sys
import datetime

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

ct = datetime.datetime.now()
print("current time: {ct}")
requests.post(
    f"{api_server}:8000/api/simulations",
    data=sim_data,
    headers={'Authorization': os.getenv('MAGNETDB_API_KEY')}
)

# how to get simu_id
r = requests.get(f"{api_server}:8000/api/simulations", headers={'Authorization': os.getenv('MAGNETDB_API_KEY')})
for simu in r.json()['items']:
    print(f"isimu_id={simu['id']}: create_at={simu['created_at']}, ct={ct}")
    # ex:2022-10-21T13:13:23.593765
    # t1 = datetime.strptime(simu['created_at'], "%Y-%m-%dT%X.%f")
    # diff = t1 - ct
    
    # # how to get user name?
    # if simu['owner']['name']:
    #     simu_id = simu['id']
    #     break
    
# # Run setup
# r = requests.post(
#     f"{api_server}:8000/api/simulations/{simu_id}",
#     data=sim_data,
#     headers={'Authorization': os.getenv('MAGNETDB_API_KEY')}
# )
