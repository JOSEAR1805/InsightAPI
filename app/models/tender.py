from django.db import models
from app.models import Setting_search

class Tender(models.Model):
  descrition = models.CharField(max_length=255)
  code = models.CharField(max_length=45)
  place_of_execution = models.CharField(max_length=255)
  awarning_authority = models.CharField(max_length=255)
  date = models.DateTimeField(auto_now_add=True)
  update_date = models.DateTimeField(auto_now=True)
  publication_date = models.DateField()
  closing_date = models.DateField()
  setting_search = models.ForeignKey(Setting_search, on_delete=models.CASCADE)

  class Meta:
    app_label = 'app'
    db_table = 'app_tender'