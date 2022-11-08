import base64
from django.db import transaction

from django.core.files.base import ContentFile
from django.shortcuts import get_list_or_404, get_object_or_404
from recipes.models import Component, Ingredient, Recipe, Tag, Favorite
from rest_framework import exceptions, serializers

from shopping_cart.models import IsInShoppingCart
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
    image = Base64ImageField(required=False, allow_null=True)

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
        fields = ('id', 'tags', 'author', 'image',
                  'ingredients', 'is_favorited', 'is_in_shopping_cart', 'name',
                  'text', 'cooking_time')

    def create(self, validated_data):
        request = self.context['request']
        validated_data['author'] = request.user
        ingredients = request.data.get('ingredients')
        tags = request.data.get('tags')
        if not ingredients or not tags:
            return exceptions.bad_request
        with transaction.atomic():
            recipe = Recipe.objects.create(**validated_data)
            for tag in tags:
                recipe.tags.add(tag)
            components_data = []
            for ingredient in ingredients:
                components_data.append(Component(
                    ingredient=Ingredient.objects.get(
                        id=ingredient.get('id')),
                    recipe=recipe,
                    quantity=ingredient.get('amount')
                    ))
            if components_data:
                Component.objects.bulk_create(components_data)
            return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.image = validated_data.get('image', instance.image)

        request = self.context.get('request')
        data = request.data
        tags = data.get('tags')
        ingredients = data.get('ingredients')

        with transaction.atomic():
            instance.tags.clear()
            instance.ingredients.clear()
            if tags:
                for tag in tags:
                    instance.tags.add(tag)
            components_data = []
            if ingredients:
                for ingredient in ingredients:
                    components_data.append(Component(
                        ingredient=Ingredient.objects.get(
                            id=ingredient.get('id')),
                        recipe=instance,
                        quantity=ingredient.get('amount')
                        ))
            if components_data:
                instance.components.all().delete()
                Component.objects.bulk_create(components_data)
        instance.save()
        return instance


class RecieptForFollowersSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']
