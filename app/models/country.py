from django.db import models

class Country(models.Model):
	name = models.CharField(max_length=255)

	class Meta:
		app_label = 'app'
		db_table = 'app_country'