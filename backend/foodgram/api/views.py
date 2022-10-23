from recipes.models import Ingredient, Recipe, Tag
from rest_framework import viewsets

from .serialisers import (IngredientsSerialisers, RecipesSerialiser,
                          TagsSerialisers)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerialisers


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerialisers


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerialiser
