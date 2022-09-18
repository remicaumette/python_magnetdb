import os
from os.path import join, isfile

from pandas import read_csv


def find_measures_files(path: str):
    found_files = []
    for file in os.listdir(path):
        file_path = join(path, file)
        if isfile(file_path):
            continue
        if file.endswith('.measures'):
            found_files.append(file_path)
            continue
        found_files = found_files + find_measures_files(file_path)
    return found_files


def get_simulation_measures(simulation_id, measure_name: str = None):

    measures_files = find_measures_files('/home/remi/Downloads/HL-test-cfpdes-thelec-Axi-sim')
    measures_names = list(map(lambda file: file.split('/').pop()[:-9], measures_files))

    for (index, measures_path) in enumerate(measures_files):
        if (measure_name is not None and not measures_path.endswith(f"{measure_name}.measures")) or index != 0:
            continue
        csv = read_csv(f"{measures_path}/values.csv")
        return {
            'measures': measures_names,
            'values': [csv.columns.tolist()] + csv.values.tolist(),
        }


print(get_simulation_measures(0))
