from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from .models import User



class AbstractUserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        r'^[\w.@+-]',
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )


class UserSerializer(AbstractUserSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "id",
            "first_name",
            "last_name",
            "is_subscribed",
        )


class LoginSerializer(AbstractUserSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )

    def validate(self, attrs):
        if attrs["username"] == "me":

            raise serializers.ValidationError(
                "Нельзя использовать 'me' в качестве username!"
            )
        return attrs


class LogoutSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = (
            "username",
            "confirmation_code",
        )
