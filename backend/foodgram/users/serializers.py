from rest_framework import serializers

from .models import Follow, User
from api import serialisers as api_serialiser


class CreateUserSerialiser(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', "first_name", "last_name", "password")

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ListRetrieveUserSerialiser(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        context = self.context.get('request')
        if context and hasattr(context.user, 'following'):
            return Follow.objects.filter(
                user=context.user,
                author=obj).exists()
        return False


class SubscribSerialiser(ListRetrieveUserSerialiser):
    reciepts = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'reciepts')
    def get_reciepts(self, obj):
        reciepts = obj.reciepts.all()
        if reciepts:
            return api_serialiser.RecieptForFollowersSerialiser(
                reciepts, many=True).data
        else:
            return {}
