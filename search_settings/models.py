from django.db import models
from rest_framework import serializers
from countries.models import Country, CountrySerializer
from categories.models import Category, CategorySerializer

# Create your models here.


class SearchSettings(models.Model):
  country = models.ForeignKey(Country, on_delete=models.CASCADE)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  description = models.CharField(max_length=255)
  url = models.CharField(max_length=255)
  created = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'setting_searchs_settingsearch'


class SearchSettingSerializer(serializers.ModelSerializer):

  category = CategorySerializer(many=False)

  country = CountrySerializer(many=False)

  class Meta:
    model = SearchSettings
    fields = ['id', 'country', 'category', 'name', 'description', 'url']
