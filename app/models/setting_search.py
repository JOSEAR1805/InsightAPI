from django.db import models
from app.models import Country, Category

class Setting_search(models.Model):
  institution_name  = models.CharField(max_length=10)
  description = models.CharField(max_length=255)
  url_web = models.CharField(max_length=255)
  country = models.ForeignKey(Country, on_delete=models.CASCADE)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)

  class Meta:
    app_label = 'app'
    db_table = 'app_setting_search'