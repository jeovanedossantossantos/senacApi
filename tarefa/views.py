import re
from django.conf import settings
from django.shortcuts import get_object_or_404, render


from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions, viewsets


from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view

from .serializer import TarefaSerializer
from .models import TarefaModel


class TarefaViews(APIView):
    serializer_class = TarefaSerializer
    # queryset = TarefaModel.objects.all()

    def get_object(self, pk):
        try:
            return TarefaModel.objects.get(pk=pk)
        except TarefaModel.DoesNotExist:
            raise Http404

    def post(self, request):
        print(request.data)
        serializer = TarefaSerializer(data=request.data)
        if serializer.is_valid():
            tarefa = serializer.save()
            return Response(TarefaSerializer(tarefa).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None, format=None):
        if id is not None:
            tarefa = self.get_object(id)
            serializer = TarefaSerializer(tarefa)
        else:
            postagens = TarefaModel.objects.all()
            serializer = TarefaSerializer(postagens, many=True)

        return Response(serializer.data)

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
