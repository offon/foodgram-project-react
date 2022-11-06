import json
import os
from recipes.models import Ingredient

def get_data_from_json():
    path = os.path.join(
        os.path.abspath(os.getcwd()), 'ingredients.json')
    print(path)
    f = open(path)
    data = json.load(f)
    f.close

    for ingr in data:
        try:
            Ingredient.objects.create(**ingr)
        except:
            pass

