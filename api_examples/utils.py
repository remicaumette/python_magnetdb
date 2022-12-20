"""
Utils for interaction with MagnetDB
"""

import json
import requests

def getlist(api_server: str, headers: dict, mtype: str='magnets', debug: bool=False) -> dict():
    """
    return list of ids for selected tpye
    """
    print(f'getlist: api_server={api_server}, mtype={mtype}')

    # loop over pages
    objects = dict()
    ids = dict()

    n = 1
    while True:
        r = requests.get(f"{api_server}/api/{mtype}s?page={n}", headers=headers)
        if r.status_code != 200:
            print(response['detail'])
            break

        response = r.json()

        # check r.json() pages max
        current_page = response['current_page']
        last_page = response['last_page']

        # get object list per page
        _page_dict = response['items']
        if debug:
            print(f'_page_dict={_page_dict}')
        for object in _page_dict:
            objects[object['name']] = object

        # increment page
        n += 1

        # break if last page is reached
        if current_page == last_page: break

    for object in objects:
        if debug:
            print(f"{mtype.upper()}: {objects[object]['name']} (id:{objects[object]['id']})")
        ids[objects[object]['name']] = objects[object]['id']

    return ids

def select(api_server: str, headers: dict, name: str, mtype: str='magnets', debug: bool=False) -> int:
    """
    return id of an object with name == name
    """

    ids = getlist(api_server, headers, mtype, debug)
    if name in ids:
        return ids[name]

    return None

def getobject(api_server: str, headers: dict, id: int, mtype: str='magnet', debug: bool=False):
    """
    return id of an object with name == name
    """
    print(f'getobject: api_server={api_server}, mtype={mtype}, id={id}')

    r = requests.get(f"{api_server}/api/{mtype}s/{id}", headers=headers)
    response = r.json()

    if r.status_code != 200:
        print(response['detail'])
        return None
    else:
        return response

def createobject(api_server: str, headers: dict, mtype: str='magnet', data: dict={}, debug: bool=False) -> int:
    """
    create an object and return its id
    """
    print(f'createobject: api_server={api_server}, mtype={mtype}, data={data}')

    r = requests.post(f"{api_server}/api/{mtype}s", data=data, headers=headers)
    response = r.json()
    if r.status_code != 200:
        print(response['detail'])
        return None
    else:
        if debug:
            print(f"{mtype.upper()} created: \n{json.dumps(response, indent=4)}")
        return response['id']
