from django.urls import include, path
from djoser.urls import authtoken
from rest_framework import routers

from users.views import CreateUserViewSet

router = routers.DefaultRouter()
router.register(r'users', CreateUserViewSet, basename='users')

urlpatterns = [
    path(r'auth/', include(authtoken)),
    path("", include(router.urls)),
]
