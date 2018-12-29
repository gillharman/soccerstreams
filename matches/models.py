from django.db import models
from datetime import date

from leagues.models import League
from teams.models import Team

class MatchQuerySet(models.QuerySet):
    def get_games(self, date=date.today()):
        return self.filter(match_date_time__date=date)


# Create your models here.
class Match(models.Model):
    SCHEDULED = 'SH'
    LIVE = 'LI'
    IN_PLAY = 'IP'
    PAUSED = 'PA'
    FINISHED = 'FN'
    POSTPONED = 'PP'
    SUSPENDED = 'SS'
    CANCELED = 'CN'
    STATUS_CHOICES = (
        (SCHEDULED, 'SCHEDULED'),
        (LIVE, 'LIVE'),
        (IN_PLAY, 'IN_PLAY'),
        (PAUSED, 'PAUSED'),
        (FINISHED, 'FINISHED'),
        (POSTPONED, 'POSTPONED'),
        (SUSPENDED, 'SUSPENDED'),
        (CANCELED, 'CANCELED'),
    )
    api_match_id = models.IntegerField()
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    match_day = models.IntegerField()
    match_date_time = models.DateTimeField()
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="homeTeam")
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="awayTeam")
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def display_name(self):
        return "{} vs {}".format(self.home_team.short_name, self.away_team.short_name)

    objects = MatchQuerySet.as_manager()