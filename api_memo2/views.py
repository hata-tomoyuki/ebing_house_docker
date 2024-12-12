from django.shortcuts import render
from rest_framework import generics, authentication, permissions

from .serializers import Memo2Serializer
from wlist.models import McModel
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response

# Create your views here.

class Memo2ViewSet(viewsets.ModelViewSet):
    queryset = McModel.objects.all()
    serializer_class = Memo2Serializer
    
    authentication_classes = (authentication.TokenAuthentication,)  ##追加
    permission_classes = (permissions.IsAuthenticated,)             ##追加

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)      ##追加