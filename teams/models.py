from django.db import models

from leagues.models import League

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=30)
    short_name = models.CharField(max_length=30)
    venue = models.CharField(max_length=30)
    club_colors = models.CharField(max_length=30)
    crest = models.CharField(max_length=2083)
    league = models.ForeignKey(League, on_delete=models.SET_NULL, null=True)