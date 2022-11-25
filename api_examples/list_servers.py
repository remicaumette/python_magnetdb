import os
import sys

import requests

api_server = os.getenv('MAGNETDB_API_SERVER') or "http://magnetdb-api.grenoble.lncmi.local"
server_name = 'calcul22'

# Run simu with ssh
r = requests.get(f"{api_server}:8000/api/servers", headers={'Authorization': os.getenv('MAGNETDB_API_KEY')})
print(f"result: type={type(r.json()['items'])}")
result_list = r.json()['items']
server_id = 12345
for (i,server) in enumerate(result_list):
    print(f'server: {server}')
    if server['name'] == server_name:
        server_id = server['id']

print(f"{server_name}: id={server_id}")

# r = requests.post(
#     f"{api_server}:8000/api/simulations/{simu_id}/run?server_id={server_id}",
#     headers={'Authorization': os.getenv('MAGNETDB_API_KEY')}
# )
