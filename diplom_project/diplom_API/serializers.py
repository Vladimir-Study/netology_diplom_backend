from django.contrib.auth.models import User
from rest_framework import serializers
from .models import FileData

class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        password = validated_data.get('password')
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        password = validated_data.get('password')
        instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'is_staff']


class FileDataSerializers(serializers.ModelSerializer):
    
    class Meta:
        model=FileData
        fields = "__all__"


class UpdateDataSerializers(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model=FileData
        fields = ['filename', 'comment', 'user']
