import os
from time import sleep

import requests

simulation_id = 6
server_id = 4

def get_simulation():
    return requests.get(
        f"http://localhost:8000/api/simulations/{simulation_id}",
        headers={'Authorization': os.getenv('MAGNETDB_API_KEY')}
    ).json()

print("Starting simulation setup...")
r = requests.post(
    f"http://localhost:8000/api/simulations/{simulation_id}/run_setup",
    headers={'Authorization': os.getenv('MAGNETDB_API_KEY')}
)
if r.status_code != 200:
    print(r.json())
    exit(1)

while True:
    simulation = get_simulation()
    if simulation['setup_status'] == 'failed':
        print('Setup failed!')
        exit(1)
    if simulation['setup_status'] == 'done':
        print('Setup done!')
        break
    print(f"Waiting setup... ({simulation['setup_status']})")
    sleep(1)

print("Starting simulation...")
r = requests.post(
    f"http://localhost:8000/api/simulations/{simulation_id}/run",
    data={'server_id': 4},
    headers={'Authorization': os.getenv('MAGNETDB_API_KEY')}
)
while True:
    simulation = get_simulation()
    if simulation['status'] == 'failed':
        print('Simulation failed!')
        exit(1)
    if simulation['status'] == 'done':
        print('Simulation done!')
        break
    print(f"Waiting the end of the simulation... ({simulation['status']})")
    sleep(10)

r = requests.get(f"http://localhost:8000/api/attachments/{simulation['log_attachment_id']}/download",
                 headers={'Authorization': os.getenv('MAGNETDB_API_KEY')})
print(r.text)
