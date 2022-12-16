import os

import requests

api_server = os.getenv('MAGNETDB_API_SERVER') or "http://magnetdb-api.grenoble.lncmi.local"

# r = requests.get(f"{api_server}:8000/api/magnets", headers={'Authorization': os.getenv('MAGNETDB_API_KEY')})
# objects = r.json()['items']

# # check r.json() to see the number of pages to get all magnets
# # response={'current_page': 1, 'last_page': 1, 'total': 13, ...
# print(f'response={r.json()}')

# loop over pages
magnets = dict()
n = 1
while True:
   r = requests.get(f"{api_server}:8000/api/magnets?page={n}", headers={'Authorization': os.getenv('MAGNETDB_API_KEY')})
   response = r.json()

   # check r.json() pages max
   current_page = response['current_page']
   last_page = response['last_page']

   # get magnet list per page
   _page_dict = response['items']

   # concat new magnet found into a global list
   magnets.update(_page_dict)

   # increment page
   n += 1

   # break if last page is reached
   if current_page == last_page: break

for magnet in magnets:
    print(f"MAGNET: {magnet['name']} (status:{magnet['status']}, id:{magnet['id']})")
