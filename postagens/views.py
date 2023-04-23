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

from .serializer import PostagemSerializer
from .models import PostagemModel


class PostagensViews(APIView):
    serializer_class = PostagemSerializer
    # queryset = PostagemModel.objects.all()

    def get_object(self, pk):
        try:
            return PostagemModel.objects.get(pk=pk)
        except PostagemModel.DoesNotExist:
            raise Http404

    def post(self, request):
        serializer = PostagemSerializer(data=request.data)
        if serializer.is_valid():
            postagem = serializer.save()
            return Response(PostagemSerializer(postagem).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None, format=None):
        if id is not None:
            user = self.get_object(id)
            serializer = PostagemSerializer(user)
        else:
            postagens = PostagemModel.objects.all()
            serializer = PostagemSerializer(postagens, many=True)

        return Response(serializer.data)

# class PostagensViews(APIView):

#     # serializer_class = PostagemSerializer
#     # queryset = PostagemModel.objects.all()
#     def get_object(self,pk):

#         try:
#             return PostagemModel.objects.get(pk=pk)
#         except PostagemModel.DoesNotExist:
#             raise Http404
#     def get(self, request, id, format=None):

#         user = self.get_object(id)
#         serializer = PostagemModel(user)
#         return Response(serializer.data)

#     def get(self, request,format=None):
#         postagens = PostagemModel.objects.all()
#         serializer =  PostagemSerializer(postagens, many=True)
#         return Response(serializer.data)
