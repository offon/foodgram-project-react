from django.contrib import admin

from .models import Component, Favorite, Ingredient, Recipe, Tag
from shopping_cart.models import IsInShoppingCart


class ComponentInline(admin.TabularInline):
    model = Component
    extra = 1


class UserAdmin(admin.ModelAdmin):
    inlines = (ComponentInline,)


class RecipeAdmin(admin.ModelAdmin):
    inlines = (ComponentInline, )


admin.site.register(Component)
admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(IsInShoppingCart)

