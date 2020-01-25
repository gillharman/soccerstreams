from django.db import models
from datetime import date

from matches.models import Match


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


class LinksQuerySet(models.QuerySet):
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

class Links(models.Model):
    match = models.ForeignKey(ScannedMatch, on_delete=models.CASCADE)
    streamer = models.CharField(max_length=100, default="")
    link = models.CharField(max_length=100, default=None)
    linkScore = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = LinksQuerySet.as_manager()


class StreamableMatchQuerySet(models.QuerySet):
    def get_games(self, date=date.today()):
        return self.filter(match__match_date_time__date=date)

class StreamableMatch(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    scanned_match = models.ForeignKey(ScannedMatch, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = StreamableMatchQuerySet.as_manager()