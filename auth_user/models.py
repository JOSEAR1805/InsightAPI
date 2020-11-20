from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers


# Create your models here.


class Privilege(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='privilege')
    tenders = models.BooleanField(default=True)
    webs = models.BooleanField(default=False)
    profiles = models.BooleanField(default=False)
    users = models.BooleanField(default=False)


class PrivilegeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Privilege
        fields = ['user', 'tenders', 'webs', 'profiles', 'users']