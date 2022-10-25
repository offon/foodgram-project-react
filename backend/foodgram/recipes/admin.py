from django.contrib import admin

from .models import Component, Ingredient, Recipe, Tag


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
