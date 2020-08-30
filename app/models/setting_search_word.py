from django.db import models
from settings_searchs.models import Setting_search

class Setting_search_word(models.Model):
  keywords = models.CharField(max_length=45)
  setting_search = models.ForeignKey(Setting_search, on_delete=models.CASCADE)

  class Meta:
    app_label = 'app'
    db_table = 'app_setting_search_word'