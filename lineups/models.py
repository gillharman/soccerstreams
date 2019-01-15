from django.db import models

from matches.models import Match

class LineupQuerySet(models.QuerySet):
    def get_home_lineup(self, match_id):
        return self.filter(match__id=match_id, lineup_type='H').order_by('id')

    def get_away_lineup(self, match_id):
        return self.filter(match__id=match_id, lineup_type='A').order_by('id')


# Create your models here.
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

    objects = LineupQuerySet.as_manager()