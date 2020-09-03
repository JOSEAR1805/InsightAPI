from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from .models import SearchSetting, SearchSettingSerializer

# Create your views here.


class SearchSettingViewSet(viewsets.ModelViewSet):
  queryset = SearchSetting.objects.all()
  serializer_class = SearchSettingSerializer
