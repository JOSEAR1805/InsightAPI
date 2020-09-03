from django.db import models
from rest_framework import serializers
from countries.models import Country
from category.models import Category

# Create your models here.


class SettingSearch(models.Model):
  country = models.ForeignKey(Country, on_delete=models.CASCADE)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  description = models.CharField(max_length=255)
  url = models.CharField(max_length=255)
  created = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)


class SettingSearchSerializer(serializers.ModelSerializer):
  class Meta:
    model = SettingSearch
    fields = ['country', 'category', 'name', 'description', 'url']
