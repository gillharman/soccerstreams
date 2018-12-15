from django.db import models

from leagues.models import League

# Create your models here.
class Team(models.Model):
    api_id = models.IntegerField()
    name = models.CharField(max_length=60)
    short_name = models.CharField(max_length=30, null=True)
    tla = models.CharField(max_length=10, null=True)
    venue = models.CharField(max_length=100, null=True)
    club_colors = models.CharField(max_length=30, null=True)
    crest = models.CharField(max_length=2083, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Teams_in_League(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)