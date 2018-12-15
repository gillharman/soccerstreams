from django.db import models

# Create your models here.
class League(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=10)
    country = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)