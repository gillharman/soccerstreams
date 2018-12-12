from django.db import models

# Create your models here.
class League(models.Model):
    name = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
