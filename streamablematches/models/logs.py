# Import django modules here.
from django.db import models

# Import soccerstreams modules here.
from .competitions import League, LeagueCopy


# Create your models here.
class RequestLogs(models.Model):
    httpStatusCode = models.CharField(max_length=10)
    requestContent = models.TextField(default=None)
    responseContent = models.TextField(default=None)
    endPoint = models.CharField(max_length=2083)
    exception = models.CharField(max_length=253)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "logs"


class RequestLog(models.Model):
    httpStatusCode = models.CharField(max_length=10)
    requestContent = models.TextField(default=None)
    responseContent = models.TextField(default=None)
    endPoint = models.CharField(max_length=2083)
    exception = models.CharField(max_length=253)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "logs_request_log"
        verbose_name = "request log"
        verbose_name_plural = "request logs"


class RotowireQuerySet(models.QuerySet):
    def get_html(self, league):
        return self.filter(league__code=league).order_by('-created').first()


class RotowireRequest(models.Model):
    html = models.TextField()
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    parsed_count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = RotowireQuerySet.as_manager()

    class Meta:
        app_label = "logs"


class RotowireRequestLog(models.Model):
    html = models.TextField()
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    parsed_count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = RotowireQuerySet.as_manager()

    class Meta:
        db_table = "logs_rotowire_request_log"
        verbose_name = "rotowire request log"
        verbose_name_plural = "rotowire request logs"
