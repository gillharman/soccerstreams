from django.contrib import admin

from .models.competitions import LineupCopy
from .models.logs import RequestLog
from .models.streamablematches import Link, StreamableMatch


# Helper methods for models below.
def scanned_match(obj):
    return "%s" % obj.scanned_match.match


def match(obj):
    return "%s" % obj.match.match


def match_name(obj):
    return "%s" % obj.match.display_name()


##########################
# models.competitions.py #
##########################
class LineupAdmin(admin.ModelAdmin):
    list_display = (match_name, 'match', 'player', 'position')
    list_filter = (
        'lineup_type',
        ('match', admin.RelatedFieldListFilter),
        ('match__home_team', admin.RelatedFieldListFilter),
        ('match__away_team', admin.RelatedFieldListFilter),
    )


##################################
# models.streamablematches.py #
##################################
class LinksAdmin(admin.ModelAdmin):
    list_display = (match,)


class StreamableMatchAdmin(admin.ModelAdmin):
    list_display = (scanned_match, match_name)


# Register models below.
admin.site.register(RequestLog)
admin.site.register(LineupCopy, LineupAdmin)
admin.site.register(Link, LinksAdmin)
admin.site.register(StreamableMatch, StreamableMatchAdmin)
