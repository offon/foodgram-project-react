from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework.authtoken.admin import TokenAdmin, TokenProxy
from django.conf import settings

from .models import Follow, User


class FollowInline(admin.TabularInline):
    model = Follow
    fk_name = "user"
    extra = 1


class UserAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_joined'
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')
    inlines = [FollowInline, ]


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


class MyToken(TokenProxy):
    @property
    def pk(self):
        return self.user_id

    class Meta:
        proxy = 'rest_framework.authtoken' in settings.INSTALLED_APPS
        abstract = 'rest_framework.authtoken' not in settings.INSTALLED_APPS
        verbose_name = "Токен"
        verbose_name_plural = "Токены"


admin.site.register(User, UserAdmin)
admin.site.register(MyToken, TokenAdmin)

admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
