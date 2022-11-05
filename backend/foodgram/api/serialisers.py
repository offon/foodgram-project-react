import base64
from django.core.exceptions import ObjectDoesNotExist
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
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)

    def get_ingredients(self, obj):
        ingredients = get_list_or_404(Component, recipe=obj)
        serialiser = ComponentSerialiser(ingredients, many=True)
        return serialiser.data

    def get_is_favorited(self, obj):
        context = self.context.get('request')
        if context and hasattr(context, 'user') and context.auth:
            return Favorite.objects.filter(
                user=context.user, is_favorited=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        context = self.context.get('request')
        if context and hasattr(context, 'user') and context.auth:
            return IsInShoppingCart.objects.filter(
                user=context.user, is_in_shopping_cart=obj).exists()
        return False

    class Meta():
        model = Recipe
        fields = ('id', 'tags', 'author', 'image',
                  'ingredients', 'is_favorited', 'is_in_shopping_cart', 'name',
                  'text', 'cooking_time')

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
                    quantity=ingredient['amount'])
            except Exception as e:
                recipe.delete()
                return exceptions.NotFound(e)
        return recipe

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if not hasattr(request, 'data'):
            raise exceptions.bad_request
        data = request.data
        shopping_cart = data.get('is_in_shopping_cart')

        if shopping_cart:
            IsInShoppingCart.objects.get_or_create(
                user=instance.author, is_in_shopping_cart=instance)
        elif shopping_cart is False:
            sc = IsInShoppingCart.objects.filter(
                user=instance.author_id, is_in_shopping_cart=instance.id)
            if sc.exists():
                IsInShoppingCart.objects.get(
                    user=instance.author_id,
                    is_in_shopping_cart=instance.id).delete()
        is_favorited = data.get('is_favorited')

        if is_favorited:
            Favorite.objects.get_or_create(
                user=instance.author, is_favorited=instance)
        elif is_favorited is False:
            favorite = Favorite.objects.filter(
                user=instance.author_id, is_favorited=instance.id)
            if favorite.exists():
                Favorite.objects.get(
                    user=instance.author_id, is_favorited=instance.id).delete()
        tags = data.get('tags')
        if tags:
            instance.tags.set([])
            for tag in tags:
                tag_for_add = get_object_or_404(Tag, id=tag)
                instance.tags.add(tag_for_add)

        ingredients = data.get('ingredients')
        components_data = []
        if ingredients and hasattr(ingredients, '__iter__'):
            for ingredient in ingredients:
                try:
                    ingredient_from_db = Ingredient.objects.get(
                        id=ingredient.get('id'))
                except:
                    raise exceptions.ValidationError('Нет такого ингредиента')
                try:
                    amount = int(ingredient.get('amount'))
                except:
                    raise exceptions.ValidationError(
                        'Не корректно задано количество ингредиента')
                components_data.append(
                    {'ingredient': ingredient_from_db,
                     'recipe': instance,
                     'amount': amount})

        if components_data:
            Component.objects.filter(recipe=instance).delete()
            for component in components_data:
                _, add_component = Component.objects.get_or_create(
                    ingredient=component.get('ingredient'),
                    recipe=component.get('recipe'),
                    quantity=component.get('amount'),
                )
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance


class RecieptForFollowersSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']

