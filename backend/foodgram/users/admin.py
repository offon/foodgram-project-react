from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Follow, User


class UserAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_joined'
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.unregister(Group)
