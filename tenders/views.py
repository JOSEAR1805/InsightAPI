from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from .models import Tender, TenderSerializer

# Create your views here.


class TenderViewSet(viewsets.ModelViewSet):
  queryset = Tender.objects.all()
  serializer_class = TenderSerializer
