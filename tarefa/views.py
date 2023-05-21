import re
from uuid import UUID
from django.conf import settings
from django.shortcuts import get_object_or_404, render
import jwt


from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions, viewsets


from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from tarefa.permissions import IsNotSuspended, ValidToken
from users.middlewares import Middlewares

from users.models import UsersModel

from .serializer import TarefaSerializer
from .models import TarefaModel


class TarefaViews(APIView):
    serializer_class = TarefaSerializer
    permission_classes = [ValidToken,IsNotSuspended]
    # queryset = TarefaModel.objects.all()
    # print(permission_classes[0])
    def get_object(self, pk, user):
        try:
            return TarefaModel.objects.get(pk=pk, user=user)
        except TarefaModel.DoesNotExist:
            raise Http404
    # def get_object(self, pk):
    #     try:
    #         return TarefaModel.objects.get(pk=pk)
    #     except TarefaModel.DoesNotExist:
    #         raise Http404

    def post(self, request):
        
        user_id=jwt.decode(request.headers.get("token"),settings.SECRET_KEY,algorithms=['HS256'])
        
        request.data["user"]=UUID(user_id['user_id'])
        serializer = TarefaSerializer(data=request.data)
        if serializer.is_valid():
            tarefa = serializer.save()
            return Response(TarefaSerializer(tarefa).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get(self, request, id=None, format=None):
    #     user_id=jwt.decode(request.headers.get("token"),settings.SECRET_KEY,algorithms=['HS256'])
       
    #     user=UUID(user_id['user_id'])
    #     if id is not None:
    #         tarefa = self.get_object(id,user)
    #         serializer = TarefaSerializer(tarefa)
    #     else:
    #         tarefas = TarefaModel.objects.filter(user=user)
    #         serializer = TarefaSerializer(tarefas, many=True)

    #     return Response(serializer.data)

    def get(self, request, id=None, format=None):
        name = request.query_params.get('name')
        user_id=jwt.decode(request.headers.get("token"),settings.SECRET_KEY,algorithms=['HS256'])
        print(user_id)
        user=UUID(user_id['user_id'])
        if id is not None:
            tarefa = self.get_object(id,user=user)
            serializer = TarefaSerializer(tarefa)
        elif name is not None:
            tarefas = TarefaModel.objects.filter(name__icontains=name, delete=False)
            serializer = TarefaSerializer(tarefas, many=True)
        else:
            tarefas = TarefaModel.objects.filter(user=user,delete=False)
            serializer = TarefaSerializer(tarefas, many=True)

        return Response(serializer.data)

    def patch(self, request, id=None):
        user_id=jwt.decode(request.headers.get("token"),settings.SECRET_KEY,algorithms=['HS256'])
       
        user=UUID(user_id['user_id'])
        tarefa = TarefaModel.objects.get(id=id,user=user)
        serializer = TarefaSerializer(tarefa, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        user_id=jwt.decode(request.headers.get("token"),settings.SECRET_KEY,algorithms=['HS256'])
       
        user=UUID(user_id['user_id'])
        tarefa = TarefaModel.objects.get(id=id,user=user)
        tarefa.delete = True
        tarefa.save()

        serializer = TarefaSerializer(tarefa)

        if serializer.data["delete"]:
            return Response({'message': "Delete success"}, status=status.HTTP_200_OK)
        
        return Response({'message': "Delete error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#  "username": "jeov" ,
# 				"email":"j@gmail.com",
# 				"password": "123"
# class PostagensViews(APIView):

#     # serializer_class = TarefaSerializer
#     # queryset = TarefaModel.objects.all()
#     def get_object(self,pk):

#         try:
#             return TarefaModel.objects.get(pk=pk)
#         except TarefaModel.DoesNotExist:
#             raise Http404
#     def get(self, request, id, format=None):

#         user = self.get_object(id)
#         serializer = TarefaModel(user)
#         return Response(serializer.data)

#     def get(self, request,format=None):
#         postagens = TarefaModel.objects.all()
#         serializer =  TarefaSerializer(postagens, many=True)
#         return Response(serializer.data)
