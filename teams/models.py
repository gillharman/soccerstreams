from django.db import models
from django.core.exceptions import ObjectDoesNotExist

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
    leagues = models.ManyToManyField(League)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_logo_url(self, dimension):
        try:
            team_logo = Team_Logo.objects.get(team=self)
        except ObjectDoesNotExist:
            print("Team logo entry for {0} not found!".format(self.name))
        else:
            if dimension == 48:
                return team_logo.logo_48x48_url
            elif dimension == 96:
                return team_logo.logo_96x96_url


class Teams_in_League(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Team_Logo(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    logo_48x48 = models.ImageField(upload_to="", null=True)
    logo_48x48_url = models.CharField(max_length=2083, null=True)
    logo_96x96 = models.ImageField(upload_to="", null=True)
    logo_96x96_url = models.CharField(max_length=2083, null=True)