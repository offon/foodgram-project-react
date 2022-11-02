from django.urls import include, path
from rest_framework import routers

from .views import IngredientViewSet, RecipeViewSet, TagViewSet, DownloadPDF, FavoritesViewSet

router = routers.DefaultRouter()
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'favorites', FavoritesViewSet, basename='favorites')

urlpatterns = [
    path('', include('users.urls')),
    path('recipes/download_shopping_cart/',
         DownloadPDF.as_view(), name='download_shopping_cart'),
    path('', include(router.urls)),
]
