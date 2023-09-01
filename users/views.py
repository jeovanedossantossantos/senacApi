from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework import generics

from tarefa.permissions import ValidAdmin, ValidToken
from .serializers import UserSerializer,UserUpdateSerializer,CustomTokenObtainPairSerializer, UsersListSerializer
from .models import UsersModel
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status
from .middlewares import Middlewares
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.views import TokenObtainPairView


from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()

                return Response({'detail': 'Logout realizado com sucesso.'})
            except Exception as e:
                return Response({'detail': 'Erro ao fazer logout.'}, status=400)

        return Response({'detail': 'O token de atualização (refresh_token) é necessário para fazer logout.'}, status=400)

class UserPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.tipo in ['client', 'root']

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class CreateUserView(generics.CreateAPIView):
    model = UsersModel

    permission_classes = [
        permissions.AllowAny
    ]
    

    serializer_class = UserSerializer
    


class UserViewsPrivate(APIView):
    permission_classes = [ValidToken]
    queryset = UsersModel.objects.all()
   
    def get_object(self,pk):
        
        try:
            return self.queryset.get(pk=pk)
        except UsersModel.DoesNotExist:
            raise Http404
  

    def put(self, request):
        
        user_id=Middlewares.decode(request.headers)
        tipo = self.get_object(user_id)
        data = UserSerializer(tipo).data
        # print(tipo)
        # print(id)
        # if(user_id == id):
        messagem = 'Changed not password'
        user = self.get_object(user_id)
        userAnt = serializer = UserSerializer(user)
        data = request.data

        
        try:
            print(data)

            if(data['password'] and user.check_password(data['password_back'])):
                user.set_password(data['password'])
                messagem="Changed password"
        except:
            messagem = 'Changed not password'
            # data['password'] = 'null'

        serializer = UserUpdateSerializer(user, data=data)
        
        
        if serializer.is_valid():
            serializer.save()
            
            return Response({"data":"Atulização com sucesso!","messagem":messagem})
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     return Response({'detail':"Não autorizado"})

class AdminView(APIView):
    permission_classes = [ValidToken,ValidAdmin]
    queryset = UsersModel.objects.all()
    def get_object(self,pk,tipo):
        
        try:
            return self.queryset.get(pk=pk,tipo=tipo)
        except UsersModel.DoesNotExist:
            raise Http404 
    # def get(self, request, id, format=None):
        
    #     user = self.get_object(id)
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)

    # class ListUsersView(generics.ListAPIView):
    
    def get(self, request,id=None, format=None):
        
        if id is not None:
            user = self.get_object(id,tipo="client")
            serializer = UsersListSerializer(user)
        else:
            users = self.queryset.filter(tipo="client")
            serializer = UsersListSerializer(users, many=True)
        
        return Response(serializer.data)
    
    def patch(self, request, id=None):
        
        user = self.get_object(id,tipo="client")
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            serializer = UsersListSerializer(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


