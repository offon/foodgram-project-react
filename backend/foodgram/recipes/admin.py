from django.contrib import admin

from .models import Ingredient, Recipe, Tag, Component
from users.models import User


class ComponentInline(admin.TabularInline):
    model = Component
    extra = 1


class UserAdmin(admin.ModelAdmin):
    inlines = (ComponentInline,)


class RecipeAdmin(admin.ModelAdmin):
    inlines = (ComponentInline, )


admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)