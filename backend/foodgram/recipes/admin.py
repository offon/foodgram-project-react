from django.contrib import admin

from .models import Component, Favorite, Ingredient, Recipe, Tag
from shopping_cart.models import IsInShoppingCart


class ComponentInline(admin.TabularInline):
    model = Component
    extra = 1


class IsFavoriteInline(admin.TabularInline):
    model = Favorite
    fk_name = "is_favorited"
    extra = 1


class IsInShoppingCartInline(admin.TabularInline):
    model = IsInShoppingCart
    fk_name = "is_in_shopping_cart"
    extra = 1


class UserAdmin(admin.ModelAdmin):
    inlines = (ComponentInline,)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'favorite_count']
    display = ['name', 'author', 'favorite_count']
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name', 'author')
    inlines = [ComponentInline, IsFavoriteInline, IsInShoppingCartInline]

    def favorite_count(self, inst):
        return inst.favorited_recipe.count()


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name', 'measurement_unit')
    search_fields = ('name', )


class ComponentAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'quantity')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_favorited')


class IsInShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_in_shopping_cart')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)

