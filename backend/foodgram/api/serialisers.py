import base64
from django.shortcuts import get_list_or_404, get_object_or_404

from django.core.files.base import ContentFile
from recipes.models import Component, Ingredient, Recipe, Tag
from rest_framework import serializers, exceptions

from users.serializers import ListRetrieveUserSerialiser


class TagsSerialisers(serializers.ModelSerializer):
    class Meta():
        model = Tag
        fields = '__all__'


class IngredientsSerialisers(serializers.ModelSerializer):
    class Meta():
        model = Ingredient
        fields = '__all__'


class ComponentSerialiser(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    measurement_unit = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    amount = serializers.IntegerField(source='quantity')

    class Meta():
        model = Component
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_measurement_unit(self, obj):
        if hasattr(obj, 'measurement_unit'):
            measurement_unit = obj.measurement_unit
        else:
            measurement_unit = obj.ingredient.measurement_unit
        return measurement_unit

    def get_name(self, obj):
        if hasattr(obj, 'name'):
            name = obj.name
        else:
            name = obj.ingredient.name
        return name

    def get_id(self, obj):
        id = obj.ingredient.id
        return id


class RecipesGetSerialiser(serializers.ModelSerializer):
    tags = TagsSerialisers(many=True, read_only=True)
    author = ListRetrieveUserSerialiser(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)

    def get_ingredients(self, obj):
        ingredients = get_list_or_404(Component, recipe=obj)
        serialiser = ComponentSerialiser(ingredients, many=True)
        return serialiser.data

    class Meta():
        model = Recipe
        exclude = ('pub_date', )

    def create(self, validated_data):
        request = self.context['request']
        validated_data['author'] = request.user
        ingredients = request.data.get('ingredients')
        if not ingredients:
            return exceptions.bad_request
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            try:
                Component.objects.create(
                    recipe=recipe,
                    ingredient=Ingredient.objects.get(id=ingredient['id']),
                    quantity=ingredient['amount']
            )
            except Exception as e:
                recipe.delete()
                return exceptions.bad_request
        return recipe


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)



    # def update(self, instance, validated_data):
    #     instance.image = validated_data.get('image', instance.image)
    #     instance.save()
    #     return instance
