from rest_framework import serializers
from .models import UsersModel
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from rest_framework.response import Response
# User = get_user_model()
from rest_framework_simplejwt.tokens import RefreshToken
# https://docs.djangoproject.com/en/4.0/ref/models/fields/
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
       
        # Usuário suspenso, retorne objeto indicando conta suspensa
        

        # Usuário não suspenso, retorne o token normalmente
        if user.suspenso:
            raise AuthenticationFailed('Suspended account')
        
        token = super().get_token(user)
        token['user_id'] = str(user.id)
        token['username'] = user.username
        token['email'] = user.email
        token['tipo'] = user.tipo
        token['suspenso'] = user.suspenso
        return token
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    tokens = serializers.SerializerMethodField()
    
    class Meta:
        model = UsersModel
        fields = ["id",'username', 'email', 'password',"tipo","suspenso","tokens"]
    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        refresh['user_id'] = str(user.id)
        refresh['username'] = user.username
        refresh['email'] = user.email
        refresh['tipo'] = user.tipo
        refresh['suspenso'] = user.suspenso
        return {
            
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    def create(self, validated_data):
        
        validated_data['password'] = make_password(validated_data.get('password'))
        validated_data['tipo']='client'
        user = super().create(validated_data)
        user.tokens = self.get_tokens(user)
        return user
       
    
    # def update(self, instance, validated_data):
    #     instance.username = validated_data.get('username', instance.username)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.tipo = validated_data.get('tipo', instance.tipo)
    #     instance.save()
    #     return instance

class UsersListSerializer(serializers.ModelSerializer):
    
    
    
    class Meta:
        model = UsersModel
        fields = ["id",'username', 'email', "tipo","suspenso"]
   