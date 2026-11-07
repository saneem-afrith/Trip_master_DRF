from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Tripdb

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tripdb
        fields = ['id', 'title', 'start_date', 'destination', 'created_by', 'created_at', 'updated_at']

    