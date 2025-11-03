from django.utils import timezone
from rest_framework import serializers

from .models import Racer, User


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "racer",
            "password",
            "password2",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields do not match"}
            )
        return attrs

    def create(self, validated_data):
        del validated_data["password2"]
        return User.objects.create_user(**validated_data)


class RacerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Racer
        fields = "__all__"
