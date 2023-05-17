from rest_framework import serializers

from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from .models import TarefaModel

class TarefaSerializer(serializers.ModelSerializer):

    class Meta:
        model = TarefaModel
        fields = ['id', 'name', 'done','delete']

    def create(self, validated_data):
        return super().create(validated_data)