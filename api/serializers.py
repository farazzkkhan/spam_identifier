from django.contrib.auth.models import User
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'email', 'password']   
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': True},
            'phone_number': {'required': True},
        }

    def create(self, validated_data):
        if User.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError({"username": "A user with that username already exists."})

        user = User.objects.create_user(
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
