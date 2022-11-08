import json
import os

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Fill data with ingredients from json file in data folder'

    def handle(self, *args, **options):
        count_ingredients = Ingredient.objects.count()
        path = os.path.join(
            os.path.abspath(os.getcwd()), 'data/ingredients.json')
        f = open(path)
        data = json.load(f)
        f.close
        ingrediets = (
            Ingredient(
                name=ingr['name'],
                measurement_unit=ingr['measurement_unit']) for ingr in data)
        Ingredient.objects.bulk_create(ingrediets, ignore_conflicts=True)

        self.stdout.write(
            'Добавлено '
            + str(Ingredient.objects.count()-count_ingredients)
            + ' ингредиентов.')
