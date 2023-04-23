from rest_framework import serializers

from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from .models import PostagemModel

class PostagemSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostagemModel
        fields = ['id', 'name', 'description']

    def create(self, validated_data):
        return super(PostagemSerializer, self).create(validated_data)