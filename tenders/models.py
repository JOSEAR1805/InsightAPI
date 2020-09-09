from django.db import models

# Create your models here.

class Tender(models.Model):
  description = models.CharField(max_length=255)
  code = models.CharField(max_length=45)
  place_of_execution = models.CharField(max_length=255)
  awarning_authority = models.CharField(max_length=255)
  date = models.DateTimeField(auto_now_add=True)
  update_date = models.DateTimeField(auto_now=True)
  publication_date = models.DateField()
  closing_date = models.DateField()

class TenderSerializer(serializers.ModelSerializer):

  class Meta:
    model = Profile
    fields = ['id', 'description', 'code', 'place_of_execution', 'awarning_authority', 
              'date', 'update_date', 'publication_date', 'closing_date']