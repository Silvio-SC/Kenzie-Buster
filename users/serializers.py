from rest_framework import serializers
from .models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)
    email = serializers.EmailField(max_length=127)
    birthdate = serializers.DateField(default=None)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    is_employee = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(read_only=True, default=False)

    def create(self, validated_data):
        if validated_data["is_employee"]:
            user = User.objects.create_superuser(**validated_data)
        else:
            user = User.objects.create_user(**validated_data)

        return user

    def update(self, instance: User, validated_data: dict):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.birthdate = validated_data.get(
            "birthdate", 
            instance.birthdate
            )
        instance.first_name = validated_data.get(
            "first_name", 
            instance.first_name
            )
        instance.last_name = validated_data.get(
            "last_name", 
            instance.last_name
            )

        instance.save()

        return instance


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)
