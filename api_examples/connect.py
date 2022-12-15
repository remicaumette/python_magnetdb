#! /usr/bin/python3

"""
Connect to MagnetDB site
"""

import os
import sys
import requests
import requests.exceptions

api_server = os.getenv('MAGNETDB_API_SERVER') or "magnetdb-api.grenoble.lncmi.local"
api_key = os.getenv('MAGNETDB_API_KEY')

def createSession(s, url: str, payload: dict={}, headers: dict={}, debug: bool=False):
    """create a request session"""

    p = s.post(url=url, data=payload, verify=True)
    if debug:
        print( f"connect: {p.url}, status={p.status_code}" )
    if p.status_code != 200:
        print(f"error {p.status_code} logging to {url_logging}" )
        sys.exit(1)
    p.raise_for_status()
    return p

def main():
    import argparse
    
    requests.packages.urllib3.disable_warnings()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", help="specify server", type=str, default=api_server)
    parser.add_argument("--port", help="specify port", type=int, default=8000)
    parser.add_argument("--type", help="select object type",
                        type=str,
                        choices=['part', 'magnet', 'site', 'record'],
                        default='magnet')
    parser.add_argument("--debug", help="activate debug mode", action='store_true')
    args = parser.parse_args()

    otype = args.type
    payload = {}
    headers = {'Authorization': os.getenv('MAGNETDB_API_KEY')}
    
    # Use 'with' to ensure the session context is closed after use.
    with requests.Session() as s:
        print(f"connect to http://{args.server}:{args.port}/api/{otype}s")
        # r = requests.get(f"http://{args.server}:{args.port}/api/{otype}s", headers=headers)
        r = s.get(f"http://{args.server}:{args.port}/api/{otype}s", headers=headers)
        print(f"{otype.upper()}: {len(r.json()['items'])} objects")
        for object in r.json()['items']:
            response = f"name={object['name']}, id:{object['id']}"
            if 'status' in object:
                response += f", status:{object['status']}"
            print(f"{otype.upper()}: {response}")
    # s.close()

if __name__ == "__main__":
    main()
