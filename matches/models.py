from django.db import models
from datetime import date

from leagues.models import League
from teams.models import Team

class MatchQuerySet(models.QuerySet):
    def get_games(self, date_=date.today()):
        return self.filter(match_date_time__date=date_)

    def get_match_display_name(self):
        d = []
        games =  self.get_games()
        for game in games:
            d.append(game.display_name())
        return d

    def get_match_from_display_name(self, string, date_=''):
        name = string.split(' vs ')
        home_team = name[0]
        away_team = name[1]
        return self.filter(home_team__short_name=home_team, away_team__short_name=away_team, match_date_time__date=date_)

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
    ace_link = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def display_name(self):
        return "{} vs {}".format(self.home_team.short_name, self.away_team.short_name)

    objects = MatchQuerySet.as_manager()