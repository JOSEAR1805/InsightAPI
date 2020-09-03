from django.db import models
from rest_framework import serializers
from countries.models import Country
from categories.models import Category

# Create your models here.


class SearchSetting(models.Model):
  country = models.ForeignKey(Country, on_delete=models.CASCADE)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  description = models.CharField(max_length=255)
  url = models.CharField(max_length=255)
  created = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)

  # class Meta:
  #   app_label = 'search_settings'
	# 	db_table = 'insight_search_setting'


class SearchSettingSerializer(serializers.ModelSerializer):
  class Meta:
    model = SearchSetting
    fields = ['country', 'category', 'name', 'description', 'url']
