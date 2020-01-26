from django.db import models
from datetime import date, datetime
import pytz


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
        app_label = "leagues"
        db_table = "league"


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

    class Meta:
        app_label = "teams"
        db_table = "team"

    def get_logo_url(self, dimension):
        try:
            team_logo = Team_Logo.objects.get(team=self)
        except Team_Logo.DoesNotExist:
            print("Team logo entry for {0} not found!".format(self.name))
        except Team_Logo.MultipleObjectsReturned as e:
            print("Multiple logo entry for {0} - {1}".format(self.name, e))
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

    class Meta:
        app_label = "teams"
        db_table = "teams_in_league"


class Team_Logo(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    logo_48x48 = models.ImageField(upload_to="", null=True)
    logo_48x48_url = models.CharField(max_length=2083, null=True)
    logo_96x96 = models.ImageField(upload_to="", null=True)
    logo_96x96_url = models.CharField(max_length=2083, null=True)

    class Meta:
        app_label = "teams"
        db_table = "team_logo"


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
        app_label = "matches"
        db_table = "match"

    def display_name(self):
        return "{} vs {}".format(self.home_team.short_name, self.away_team.short_name)

    objects = MatchQuerySet.as_manager()


class GamesQuerySet(models.QuerySet):
    def get_games(self, date=date.today()):
        return self.filter(created__date=date).distinct('match')

    def get_match_name(self, gameID):
        return self.get(id=gameID).match


class ScannedMatch(models.Model):
    match = models.CharField(max_length=100)
    postUrl = models.CharField(max_length=2083, default='https://reddit.com/soccerstreams')
    time = models.CharField(max_length=14)
    aceLink = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = GamesQuerySet.as_manager()

    class Meta:
        db_table = "scanned_match"


class LinkQuerySet(models.QuerySet):
    def get_links(self, gameID):
        return self.filter(match=gameID).distinct('link') #Workaround implemented due to data duplication

    def get_streamers(self, gameID):
        links = self.get_links(gameID)
        return self.filter(id__in=links).values('streamer', 'linkScore').annotate(models.Count('streamer'))

    def get_values(self, key, value, field):
        q = {key:value}
        return self.filter(**q).values_list(field, flat=True)

    def get_count(self, key, value):
        q = {key:value}
        return self.filter(**q).count()


class Link(models.Model):
    match = models.ForeignKey(ScannedMatch, on_delete=models.CASCADE)
    streamer = models.CharField(max_length=100, default="")
    link = models.CharField(max_length=100, default=None)
    linkScore = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = LinkQuerySet.as_manager()

    class Meta:
        db_table = "link"


class StreamableMatchQuerySet(models.QuerySet):
    def get_games(self, date=date.today()):
        return self.filter(match__match_date_time__date=date)


class StreamableMatch(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    scanned_match = models.ForeignKey(ScannedMatch, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = StreamableMatchQuerySet.as_manager()

    class Meta:
        db_table = "streamable_match"
