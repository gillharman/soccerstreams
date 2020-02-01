# Import python modules here.
from datetime import date, datetime
import pytz

# Import django modules here.
from django.db import models
from django.db.models import Q


# Create your models here.
class League(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=10)
    country = models.CharField(max_length=30)
    api_id = models.IntegerField(null=True)
    tracked = models.BooleanField(default=False)
    current_match_day = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "competitions_league"
        verbose_name = "league"
        verbose_name_plural = "leagues"


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

    class Meta:
        db_table = "competitions_team"
        verbose_name = "team"
        verbose_name = "teams"

    def get_logo_url(self, dimension):
        try:
            team_logo = TeamLogo.objects.get(team=self)
        except TeamLogo.DoesNotExist:
            print("Team logo entry for {0} not found!".format(self.name))
        except TeamLogo.MultipleObjectsReturned as e:
            print("Multiple logo entry for {0} - {1}".format(self.name, e))
        else:
            if dimension == 48:
                return team_logo.logo_48x48_url
            elif dimension == 96:
                return team_logo.logo_96x96_url


class TeamInLeague(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "competitions_team_in_league"
        verbose_name = "team in league"
        verbose_name_plural = "team in leagues"


class TeamLogo(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    logo_48x48 = models.ImageField(upload_to="", null=True)
    logo_48x48_url = models.CharField(max_length=2083, null=True)
    logo_96x96 = models.ImageField(upload_to="", null=True)
    logo_96x96_url = models.CharField(max_length=2083, null=True)

    class Meta:
        db_table = "competitions_team_logo"
        verbose_name = "team logo"
        verbose_name_plural = "team logos"


class MatchQuerySet(models.QuerySet):
    def get_games(self, date_=datetime.today()):
        date_ = date_.replace(tzinfo=pytz.utc)
        return self.filter(match_date_time__date=date_)

    def get_match_display_name(self):
        d = []
        games = self.get_games()
        for game in games:
            d.append(game.display_name())
        return d

    def get_match_from_display_name(self, string, date_=''):
        name = string.split(' vs ')
        home_team = name[0]
        away_team = name[1]
        return self.filter(home_team__short_name=home_team, away_team__short_name=away_team, match_date_time__date=date_)


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
        (SCHEDULED, 'Scheduled'),
        (LIVE, 'Live'),
        (IN_PLAY, 'In Play'),
        (PAUSED, 'Paused'),
        (FINISHED, 'Finished'),
        (POSTPONED, 'Postponed'),
        (SUSPENDED, 'Suspended'),
        (CANCELED, 'Canceled'),
    )

    HOME_TEAM = 'HO'
    AWAY_TEAM = 'AT'
    DRAW = 'DW'

    WINNER_CHOICES = (
        (HOME_TEAM, 'Home Team'),
        (AWAY_TEAM, 'Away Team'),
        (DRAW, 'Draw')
    )

    api_match_id = models.IntegerField()
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    match_day = models.IntegerField()
    match_date_time = models.DateTimeField()
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="homeTeam")
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="awayTeam")
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    goals_scored_home_team = models.IntegerField(null=True)
    goals_scored_away_team = models.IntegerField(null=True)
    penalty_goals_home_team = models.IntegerField(null=True)
    penalty_goals_away_team = models.IntegerField(null=True)
    winner = models.CharField(max_length=2, choices=WINNER_CHOICES, default="")
    ace_link = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "competitions_match"
        verbose_name = "match"
        verbose_name_plural = "matches"

    def display_name(self):
        return "{} vs {}".format(self.home_team.short_name, self.away_team.short_name)

    objects = MatchQuerySet.as_manager()


class LineupQuerySet(models.QuerySet):
    def get_home_lineup(self, match_id):
        return self.filter(match__id=match_id, lineup_type='H').order_by('id')

    def get_away_lineup(self, match_id):
        return self.filter(match__id=match_id, lineup_type='A').order_by('id')

    def get_lineup(self, match_id, team_id):
        return self.filter(match__id=match_id).filter(Q(match__home_team__id=team_id) | Q(match__away_team__id=team_id)).order_by('id')


class Lineup(models.Model):
    POSITIONS = (
        ('G', 'Goalkeeper'),
        ('D', 'Defender'),
        ('M', 'Midfielder'),
        ('F', 'Forward'),
        ('F/M', 'Forward/Midfielder'),
        ('M/D', 'Midfielder/Defender')
    )
    LINEUP_TYPES = (
        ('H', 'Home'),
        ('A', 'Away')
    )
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    position = models.CharField(max_length=40, choices=POSITIONS)
    player = models.CharField(max_length=40)
    lineup_type = models.CharField(max_length=10, choices=LINEUP_TYPES)
    confirmed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "competitions_lineup"
        verbose_name = "lineup"
        verbose_name_plural = "lineups"

    objects = LineupQuerySet.as_manager()
