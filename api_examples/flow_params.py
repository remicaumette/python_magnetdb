import requests
import requests.exceptions
import tempfile
import re

import utils
import pandas as pd
from txt2csv import load_files

def compute(api_server: str, headers: dict, id: int, mtype: str='magnet', debug: bool=False):
    """
    compute flow_params for a given objet (magnet/site)
    """
    print(f'flow_params.compute: api_server={api_server}, mtype={mtype}, id={id}')

    # default value
    flow_params = {
        "Vp0": { "value" : 1000, "unit": "rpm"},
        "Vpmax": { "value" : 2840, "unit": "rpm"},
        "F0": { "value" : 0, "unit": "l/s"},
        "Fmax": { "value" : 61.71612272405876 , "unit": "l/s"},
        "Pmax": { "value" : 22, "unit": "bar"},
        "Pmin": { "value" : 4, "unit": "bar"},
        "Imax": { "value" : 28000, "unit": "A"}
    }
        
    fit_data = {
        'M9': { 'Rpm': 'Rpm1', 'Flow': 'Flow1', 'rlist' : []},
        'M10': { 'Rpm': 'Rpm2', 'Flow': 'Flow2', 'rlist' : []},
    }

    records = utils.gethistory(api_server, headers, id, mtype, debug)
    if debug:
        print(f'records: {records}')

    for key in fit_data:
        fit_data[key]['rlist'] = [record for record in records if key in record['name']]

        # create a temp directory
        # download files
        files = []
        for f in fit_data[key]['rlist']:
            print(f'f={f}')
            id = f['id']
            data = utils.getobject(api_server, headers, id=id, mtype='record', debug=debug)
            
            with tempfile.TemporaryDirectory() as tempdir:
                attach = f['attachment_id']
                files.append(utils.download(api_server, headers, attach, debug))

        # df = load_files(files, show=debug, debug=debug)
        # Ikey = "tttt"
        # if not Get_Ikey:
        #     # get first Icoil column (not necessary Icoil1)
        #     keys = df.columns.values.tolist()
                
        #     # key firs header that match Icoil\d+
        #     for _key in keys:
        #         _found = re.match("Icoil\d+", _key)
        #         if _found:
        #             Ikey = _found.group()
        #             print(f"Ikey={Ikey}")
        #             Get_Ikey = True
        #             break

        # pairs = [f"{Ikey}-{fit_data[key]['Rpm']}"]
        # # plot_key_vs_key(df, pairs, show=True)

        # import numpy as np
        # from scipy import optimize

        # Imax = flow_params['Imax']['value'] # 28000
        # def vpump_func(x, a, b):
        #     return a * (x/Imax)**2 + b

        # df.replace([np.inf, -np.inf], np.nan, inplace=True)
        # df.dropna(inplace=True)

        # # # drop values for Icoil1 > Imax
        # result = df.query(f'{Ikey} <= 28000.') #, inplace=True)
        # if result is not None:
        #     print(f'df: nrows={df.shape[0]}, results: nrows={result.shape[0]}')
        
        # x_data = result[f'{Ikey}'].to_numpy()
        # y_data = result[fit_data[key]['Rpm']].to_numpy()
        # params, params_covariance = optimize.curve_fit(vpump_func, x_data, y_data) #, p0=[flow_params['Vp0']['value'], flow_params['Vpmax']['value'] = params[1]])
        # print(f'result params: {params}')
        # print(f'result covariance: {params_covariance}')
        # print(f'result stderr: {np.sqrt(np.diag(params_covariance))}')
        # flow_params['Vp0']['value'] = params[0]
        # flow_params['Vpmax']['value'] = params[1]

        # # save flow_params
        # import json
        # filename = f"{magnet_name}-{site_data['name']}-{key}-flow_params.json"
        # with open(filename, 'w') as f:
        #     f.write(json.dumps(flow_params, indent=4))
       
        
        
    
    
