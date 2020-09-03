from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from .models import WordsSearchSetting, WordsSearchSettingSerializer

# Create your views here.


class WordsSearchSettingViewSet(viewsets.ModelViewSet):
  queryset = WordsSearchSetting.objects.all()
  serializer_class = WordsSearchSettingSerializer
