from django.shortcuts import get_object_or_404

from recipes.models import Ingredient, Recipe, Tag
from rest_framework import status, viewsets
from rest_framework.response import Response

from .permissions import AuthorOrReadOnly
from .serialisers import (IngredientsSerialisers, RecipesGetSerialiser,
                           TagsSerialisers)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerialisers


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerialisers


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesGetSerialiser
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [AuthorOrReadOnly, ]

    # def create(self, request):
    #     serialiser = RecipesPostPatchSerialiser(data=request.data)
    #     if serialiser.is_valid(raise_exception=True):
    #         tags = []
    #         components=[]
    #         for tag in request.data.get('tags'):
    #             tags.append(get_object_or_404(Tag, id=tag))
    #         ingredients = request.data.get('ingredients')
    #         serialiser.save(author=request.user, tags=tags)
    #         for ingredient in ingredients:
    #             component= Component.objects.create(
    #                 recipe = serialiser.instance,
    #                 ingredient=get_object_or_404(Ingredient,pk=ingredient.get('id')),
    #                 quantity=ingredient.get('amount'))
    #             components.append(component)
    #         serialiser.save(ingredient=components)
    #         return Response(serialiser.data, status=status.HTTP_201_CREATED)

