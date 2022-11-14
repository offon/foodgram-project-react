import base64

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.db import transaction
from django.shortcuts import get_list_or_404
from rest_framework import exceptions, serializers

from recipes.models import Component, Ingredient, Recipe, Tag
from users.serializers import ListRetrieveUserSerialiser


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class TagsSerialisers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientsSerialisers(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class ComponentSerialiser(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    measurement_unit = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    amount = serializers.IntegerField(source='quantity')

    class Meta:
        model = Component
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_measurement_unit(self, obj):
        if hasattr(obj, 'measurement_unit'):
            measurement_unit = obj.measurement_unit
        measurement_unit = obj.ingredient.measurement_unit
        return measurement_unit

    def get_name(self, obj):
        if hasattr(obj, 'name'):
            return obj.name
        return obj.ingredient.name

    def get_id(self, obj):
        return obj.ingredient.id


class RecipesGetSerialiser(serializers.ModelSerializer):
    tags = TagsSerialisers(many=True, read_only=True)
    author = ListRetrieveUserSerialiser(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    def get_ingredients(self, obj):
        ingredients = get_list_or_404(Component, recipe=obj)
        serialiser = ComponentSerialiser(ingredients, many=True)
        return serialiser.data

    def get_is_favorited(self, obj):
        context = self.context.get('request')
        if context and hasattr(context, 'user') and context.auth:
            return context.user.is_favorited.filter(is_favorited=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        context = self.context.get('request')
        if context and hasattr(context, 'user') and context.auth:
            return context.user.is_in_shopping_cart.filter(
                is_in_shopping_cart=obj).exists()
        return False

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'image',
                  'ingredients', 'is_favorited', 'is_in_shopping_cart', 'name',
                  'text', 'cooking_time']


class ComponentInRecipe(serializers.BaseSerializer):
    def to_internal_value(self, data):
        id = data.get('id')
        quantity = data.get('amount')
        recipe = self.context.get('recipe')

        try:
            ingredien = Ingredient.objects.get(id=id)
        except(ValueError, ObjectDoesNotExist):
            raise serializers.ValidationError({
                'id': 'Не правильно указан ингридиент.'
            })
        if not quantity:
            raise serializers.ValidationError({
                'amount': 'Обязательное поле.'
            })
        if not recipe:
            raise serializers.ValidationError({
                'recipe': 'Обязательное поле.'
            })
        return {
            'ingredient': ingredien,
            'recipe': recipe,
            'quantity': quantity
        }

    def create(self, validated_data):
        return Component.objects.create(**validated_data)


class RecipeCreateUpdate(serializers.ModelSerializer):
    author = ListRetrieveUserSerialiser(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'image',
                  'ingredients', 'name',
                  'text', 'cooking_time', 'image']

    def create(self, validated_data):
        request = self.context['request']
        validated_data['author'] = request.user
        ingredients = request.data.get('ingredients')
        tags = validated_data.pop('tags')
        with transaction.atomic():
            recipe = Recipe.objects.create(**validated_data)
            recipe.tags.set(tags)
            components = ComponentInRecipe(
                data=ingredients,
                many=True,
                context={'recipe': recipe})
            if components.is_valid(raise_exception=True):
                components.save()
                return recipe
            return exceptions.bad_request

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.image = validated_data.get('image', instance.image)
        instance.tags.set(validated_data.get('tags', instance.tags))

        request = self.context.get('request')
        ingredients = request.data.get('ingredients')

        with transaction.atomic():
            instance.ingredients.clear()
            components = ComponentInRecipe(
                data=ingredients,
                many=True,
                context={'recipe': instance})
            if components.is_valid(raise_exception=True):
                components.save()
            instance.save()
        return instance


class RecieptForFollowersSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']
