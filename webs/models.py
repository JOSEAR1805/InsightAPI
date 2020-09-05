from django.db import models
from rest_framework import serializers
from countries.models import Country

# Create your models here.


class Web(models.Model):
  country = models.ForeignKey(Country, on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  url = models.CharField(max_length=255)
  comments = models.CharField(max_length=255)
  created = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)


class WebSerializer(serializers.ModelSerializer):
  # country = CountrySerializer(many=False)

  class Meta:
    model = Web
    fields = ['id', 'country', 'name', 'url', 'comments']