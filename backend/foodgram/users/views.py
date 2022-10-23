from multiprocessing import context
from django.shortcuts import get_object_or_404
from djoser import utils
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import CreateUserSerialiser, ListRetrieveUserSerialiser


class CreateUserViewSet(viewsets.ViewSet):
    @action(
        detail=False,
        methods=['get', ],
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = ListRetrieveUserSerialiser(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        ["post", ],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def set_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()
        utils.logout_user(self.request)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        queryset = User.objects.all()
        serializer = ListRetrieveUserSerialiser(
            queryset, many=True, context={'request': request})

        return Response(serializer.data)

    def create(self, request):
        serializer = CreateUserSerialiser(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ListRetrieveUserSerialiser(user, context={'request': request})
        return Response(serializer.data)
