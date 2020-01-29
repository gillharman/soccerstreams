from django.contrib import admin
from streamablematches.models.competitions import LineupCopy


def match_name(obj):
    return "%s" % (obj.match.display_name())


# Register your models here.
class LineupAdmin(admin.ModelAdmin):
    list_display = (match_name, 'match', 'player', 'position')
    list_filter = (
        'lineup_type',
        ('match', admin.RelatedFieldListFilter),
        ('match__home_team', admin.RelatedFieldListFilter),
        ('match__away_team', admin.RelatedFieldListFilter),
    )


admin.site.register(LineupCopy, LineupAdmin)
