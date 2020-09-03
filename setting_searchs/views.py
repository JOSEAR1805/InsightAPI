from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from .models import SettingSearch, SettingSearchSerializer

# Create your views here.


class SettingSearchViewSet(viewsets.ModelViewSet):
  queryset = SettingSearch.objects.all()
  serializer_class = SettingSearchSerializer
