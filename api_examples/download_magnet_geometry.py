import os
import re

import requests

r = requests.get("http://localhost:8000/api/magnets/1", headers={'Authorization': os.getenv('MAGNETDB_API_KEY')})
data = r.json()
if r.status_code != 200:
    print(data)
    exit(1)

print(f"attachment id found: f{data['geometry_attachment_id']}")
r = requests.get(f"http://localhost:8000/api/attachments/{data['geometry_attachment_id']}/download",
                 headers={'Authorization': os.getenv('MAGNETDB_API_KEY')})

filename = list(re.finditer(r"filename=\"(.+)\"", r.headers['content-disposition'], re.MULTILINE))[0].group(1)
with open(filename, 'w+') as file:
    file.write(r.text)
