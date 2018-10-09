from django.db import models

class GamesQuerySet(models.QuerySet):
    def get_games(self):
        return self.all()

class Game(models.Model):
    match = models.CharField(max_length=100)
    url = models.CharField(max_length=2083, default='https://reddit.com/soccerstreams')
    time = models.CharField(max_length=14)

    objects = GamesQuerySet.as_manager()


class Logs(models.Model):
    httpStatusCode = models.CharField(max_length=10)
    requestContent = models.TextField(default=None)
    responseContent = models.TextField(default=None)
    endPoint = models.CharField(max_length=2083)
    exception = models.CharField(max_length=253)