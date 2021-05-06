from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from taskbord.models import CustomUser, Cards


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password']


class CardSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )
    executor = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Cards
        fields = ['id', 'creator', 'executor', 'status', 'text', 'change_time']
