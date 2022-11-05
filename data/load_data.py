import json
import os


def get_data_from_json():
    path = os.path.join(
        os.path.abspath(os.getcwd()), 'data/ingredients.json')
    print(path)
    f = open(path)
    data = json.load(f)
    f.close
    return data
