from django.contrib import admin

from streamablematches.models.competitions import TeamsInLeagueCopy, TeamLogoCopy, TeamCopy


def team(obj):
    return "%s" % obj.team.name


def league(obj):
    return "%s" % obj.league.name


def leagues(obj):
    return "%s" % list(obj.leagues.all().values_list('name', flat=True))


# Register your models here.
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', leagues)
    # date_hierarchy = 'created'


class TeamInLeagueAdmin(admin.ModelAdmin):
    list_display = ('team', team, league, 'created', 'updated')


class TeamLogoAdmin(admin.ModelAdmin):
    list_display = ('id', team, 'logo_48x48', 'logo_48x48_url', 'logo_96x96', 'logo_96x96_url')
    # list_display_links = None


admin.site.register(TeamsInLeagueCopy, TeamInLeagueAdmin)
admin.site.register(TeamLogoCopy, TeamLogoAdmin)
admin.site.register(TeamCopy, TeamAdmin)
