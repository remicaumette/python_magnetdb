from os import getenv

import requests

api_url = getenv("API_URL", "http://localhost:8000")


def load_object_from_api(object_type: str, object_id: str):
    url = f"{api_url}/api/{object_type}/{object_id}/config"
    print(f"calling {url}...")
    req = requests.get(url)
    if req.status_code != requests.codes.ok:
        raise Exception(f"Failed to retrieve {object_type}_{object_id} from api")

    return req.json()


def load_attachment(attachment_id: int):
    url = f"{api_url}/api/attachments/{attachment_id}/download"
    print(f"calling {url}...")
    req = requests.get(url)
    if req.status_code != requests.codes.ok:
        raise Exception(f"Failed to retrieve attachment {attachment_id} from api")

    return req.content
