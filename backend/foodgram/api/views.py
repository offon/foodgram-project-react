
from django.shortcuts import get_object_or_404

from rest_framework import permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .permissions import AuthorOrReadOnly
from .serialisers import (IngredientsSerialisers, RecipesGetSerialiser,
                          TagsSerialisers)
from recipes.models import Favorite, Ingredient, Recipe, Tag
from shopping_cart.models import IsInShoppingCart
from shopping_cart.utils import shopping_cart_pdf


class DownloadPDF(views.APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        return shopping_cart_pdf(request.user)


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

    @action(methods=['delete', 'post'], detail=True)
    def favorite(self, request, pk=None):
        if self.request.method == 'POST':
            recipe = get_object_or_404(
                Recipe, pk=pk)
            _, created = Favorite.objects.get_or_create(
                user=request.user, is_favorited=recipe)
            if created:
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            recipe = get_object_or_404(
                Recipe, pk=pk)
            favorite = get_object_or_404(Favorite, is_favorited=recipe)
            favorite.delete()
            return Response(status=status.HTTP_200_OK)

    @action(methods=['delete', 'post'], detail=True)
    def shopping_cart(self, request, pk=None):
        if self.request.method == 'POST':
            recipe = get_object_or_404(
                Recipe, pk=pk)
            _, created = IsInShoppingCart.objects.get_or_create(
                user=request.user, is_in_shopping_cart=recipe)
            if created:
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            recipe = get_object_or_404(
                Recipe, pk=pk)
            favorite = get_object_or_404(
                IsInShoppingCart,
                is_in_shopping_cart=recipe)
            favorite.delete()
            return Response(status=status.HTTP_200_OK)
