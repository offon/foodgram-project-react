from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Favorite, Ingredient, Recipe, Tag
from rest_framework import filters, permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from shopping_cart.models import IsInShoppingCart
from shopping_cart.utils import shopping_cart_pdf

from .permissions import AuthorOrReadOnly
from .serialisers import (IngredientsSerialisers, RecipesGetSerialiser,
                          TagsSerialisers)


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
    serializer_class = RecipesGetSerialiser
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [AuthorOrReadOnly, ]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('tags__slug', )
    search_fields = ('name', )
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Recipe.objects.all()
        if self.request.query_params.get('is_favorited'):
            reciepts_str_list = self.request.user.is_favorited.all().values_list(
                    'is_favorited', flat=True)
            queryset = Recipe.objects.filter(
                pk__in=reciepts_str_list)
        if self.request.query_params.get('is_in_shopping_cart'):
            reciepts_str_list = self.request.user.is_in_shopping_cart.all().values_list(
                    'is_in_shopping_cart', flat=True)
            queryset = Recipe.objects.filter(
                pk__in=reciepts_str_list)
        return queryset

    @action(methods=['delete', 'post'], detail=True)
    def favorite(self, request, pk=None):
        if self.request.method == 'POST':
            recipe = get_object_or_404(
                Recipe, pk=pk)
            Favorite.objects.get_or_create(
                user=request.user, is_favorited=recipe)
            return Response(status=status.HTTP_200_OK)
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
            IsInShoppingCart.objects.get_or_create(
                user=request.user, is_in_shopping_cart=recipe)
            return Response(status=status.HTTP_200_OK)
        recipe = get_object_or_404(
            Recipe, pk=pk)
        favorite = get_object_or_404(
            IsInShoppingCart,
            is_in_shopping_cart=recipe)
        favorite.delete()
        return Response(status=status.HTTP_200_OK)


class FavoritesViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', ]
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = RecipesGetSerialiser
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('tags__slug', 'is_favorited')
    search_fields = ('name', )

    def get_queryset(self):
        reciepts_str_list = self.request.user.is_favorited.all().values_list(
            'is_favorited', flat=True)
        reciepts = Recipe.objects.filter(
            pk__in=reciepts_str_list)
        return reciepts
