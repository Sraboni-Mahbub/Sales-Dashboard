from django.shortcuts import render
from rest_framework import generics
from authenticate.models import *
from homedash.models import *
from .serializers import UserProfileSerializer

# Create your views here.

class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

