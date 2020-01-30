from django.contrib import admin

from .models.competitions import (
    LeagueCopy, LineupCopy, TeamCopy, TeamLogoCopy, TeamsInLeagueCopy
)
from .models.logs import RequestLog
from .models.streamablematches import Link, StreamableMatch


# Helper methods for models below.
def league(obj):
    return "%s" % obj.league.name


def leagues(obj):
    return "%s" % list(obj.leagues.all().values_list('name', flat=True))


def scanned_match(obj):
    return "%s" % obj.scanned_match.match


def match(obj):
    return "%s" % obj.match.match


def match_name(obj):
    return "%s" % obj.match.display_name()


def team(obj):
    return "%s" % obj.team.name


##########################
# models.competitions.py #
##########################
class LeagueAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "tracked")


class LineupAdmin(admin.ModelAdmin):
    list_display = (match_name, 'match', 'player', 'position')
    list_filter = (
        'lineup_type',
        ('match', admin.RelatedFieldListFilter),
        ('match__home_team', admin.RelatedFieldListFilter),
        ('match__away_team', admin.RelatedFieldListFilter),
    )


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', leagues)
    # date_hierarchy = 'created'


class TeamLogoAdmin(admin.ModelAdmin):
    list_display = ('id', team, 'logo_48x48', 'logo_48x48_url', 'logo_96x96', 'logo_96x96_url')
    # list_display_links = None


class TeamInLeagueAdmin(admin.ModelAdmin):
    list_display = ('team', team, league, 'created', 'updated')


##################################
# models.streamablematches.py #
##################################
class LinksAdmin(admin.ModelAdmin):
    list_display = (match,)


class StreamableMatchAdmin(admin.ModelAdmin):
    list_display = (scanned_match, match_name)


# Register models below.
admin.site.register(RequestLog)
admin.site.register(LeagueCopy, LeagueAdmin)
admin.site.register(LineupCopy, LineupAdmin)
admin.site.register(Link, LinksAdmin)
admin.site.register(StreamableMatch, StreamableMatchAdmin)
admin.site.register(TeamCopy, TeamAdmin)
admin.site.register(TeamsInLeagueCopy, TeamInLeagueAdmin)
admin.site.register(TeamLogoCopy, TeamLogoAdmin)
