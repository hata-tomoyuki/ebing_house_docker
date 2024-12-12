from django.shortcuts import render
from rest_framework import generics, authentication, permissions

from api_user import serializers

from django.db.models import Q
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response

# Create your views here.

class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer


# class Memo1ViewSet(viewsets.ModelViewSet):
#     queryset = MemoModel.objects.all()
#     serializer_class = Memo1Serializer
    