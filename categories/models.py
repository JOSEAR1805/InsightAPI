from django.db import models
from rest_framework import serializers
from countries.models import Country

# Create your models here.


class Category(models.Model):
  country = models.ForeignKey(Country, on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  created = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'category_category'


class CategorySerializer(serializers.ModelSerializer):
  # country = serializers.StringRelatedField(many=False)

  class Meta:
    model = Category
    fields = ['id', 'name', 'country']
