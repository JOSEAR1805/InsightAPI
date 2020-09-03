from django.db import models
from rest_framework import serializers
from search_settings.models import SearchSetting

# Create your models here.


class WordsSearchSetting(models.Model):
  search_setting = models.ForeignKey(SearchSetting, on_delete=models.CASCADE)
  word = models.CharField(max_length=255)
  created = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)

  # class Meta:
  #   app_label = 'words_search_settings'
	# 	db_table = 'insight_word_search_setting'


class WordsSearchSettingSerializer(serializers.ModelSerializer):
  class Meta:
    model = WordsSearchSetting
    fields = ['id', 'search_setting', 'word']
