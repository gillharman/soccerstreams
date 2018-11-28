from django.db import models

from datetime import date

class GamesQuerySet(models.QuerySet):
    def get_games(self):
        # d = date.today()
        d = date(2018, 11, 10)
        return self.filter(created__date=d).distinct('match')

    def get_match_name(self, gameID):
        return  self.get(id=gameID).match

class LinksQuerySet(models.QuerySet):
    def get_links(self, gameID):
        return self.filter(match=gameID).distinct('link')

    def get_values(self, key, value, field):
        q = {key:value}
        return self.filter(**q).values_list(field, flat=True)

    def get_count(self, key, value):
        q = {key:value}
        return self.filter(**q).count()

class Game(models.Model):
    match = models.CharField(max_length=100)
    postUrl = models.CharField(max_length=2083, default='https://reddit.com/soccerstreams')
    time = models.CharField(max_length=14)
    aceLink = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = GamesQuerySet.as_manager()

class Links(models.Model):
    match = models.ForeignKey(Game, on_delete=models.CASCADE)
    streamer = models.CharField(max_length=100, default=None)
    link = models.CharField(max_length=100, default=None)
    linkScore = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = LinksQuerySet.as_manager()

class Logs(models.Model):
    httpStatusCode = models.CharField(max_length=10)
    requestContent = models.TextField(default=None)
    responseContent = models.TextField(default=None)
    endPoint = models.CharField(max_length=2083)
    exception = models.CharField(max_length=253)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)