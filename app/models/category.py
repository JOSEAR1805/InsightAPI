from django.db import models
from app.models import Country

class Category(models.Model):
  name = models.CharField(max_length=50)
  description = models.CharField(max_length=255)
  country = models.ForeignKey(Country, blank=True, on_delete=models.CASCADE)

  class Meta:
    app_label = 'app'
    db_table = 'app_category'