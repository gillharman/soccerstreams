from django.db import models

from datetime import date

class GamesQuerySet(models.QuerySet):
    def get_games(self):
        d = date(2018, 11, 4)
        return self.filter(
            created__date = d
            # date.today()
        )

class Game(models.Model):
    match = models.CharField(max_length=100)
    postUrl = models.CharField(max_length=2083, default='https://reddit.com/soccerstreams')
    time = models.CharField(max_length=14)
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

class Logs(models.Model):
    httpStatusCode = models.CharField(max_length=10)
    requestContent = models.TextField(default=None)
    responseContent = models.TextField(default=None)
    endPoint = models.CharField(max_length=2083)
    exception = models.CharField(max_length=253)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)