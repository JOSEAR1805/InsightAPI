from django.db import models
from rest_framework import serializers

# Create your models here.


class Country(models.Model):
  name = models.CharField(max_length=255)
  created = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)


class CountrySerializer(serializers.HyperlinkedModelSerializer):

  class Meta:
    model = Country
    fields = ['id', 'name']
