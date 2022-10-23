import base64

from django.core.files.base import ContentFile
from recipes.models import Ingredient, Tag, Recipe
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class TagsSerialisers(serializers.ModelSerializer):
    class Meta():
        model = Tag
        fields = '__all__'


class IngredientsSerialisers(serializers.ModelSerializer):
    class Meta():
        model = Ingredient
        fields = '__all__'


class RecipesSerialiser(serializers.ModelSerializer):
    class Meta():
        model = Recipe
        fields = '__all__'