from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from django.core import serializers
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from streamablematches.forms import AceStreamForm
from .models import Links, StreamableMatch, ScannedMatch
from teams.models import Team_Logo
from matches.models import Match
from lineups.models import Lineup
from leagues.models import League
from utils import (
    is_mobile, team_info, lineup_info
)

from .forms import AceStreamForm

def welcome(request):
    return render(request, 'games/templates/welcome.html')


def league_matches(request, league="PL"):
    _is_mobile = is_mobile(request)
    games = Match.objects.filter(league__code=league).order_by('match_day', 'match_date_time')
    try:
        league = League.objects.get(code=league)
    except League.DoesNotExist:
        league = League.objects.filter(code=league).first()

    return render(request, 'games/templates/league_matches.html',
                  {"data": {
                      "is_mobile_tablet": is_mobile,
                      "matches": games,
                      "league": league,
                  }})

# def ajax_league_matches(request):
#     league = request.GET['league']
#     # print(league)
#     is_mobile = isMobile(request)
#     games = Match.objects.filter(league__code=league).order_by('match_day')
#     return render(request, 'games/templates/league_matches.html',
#                   {"data": {
#                       "is_mobile_tablet": is_mobile,
#                       "matches": games,
#                   }})


def watch_game(request, match_id):
    _is_mobile = is_mobile(request)
    streamable_game = StreamableMatch.objects.filter(match__id=match_id).first()
    links = []
    if streamable_game:
        links = Links.objects.get_links(streamable_game.scanned_match.id)
    match =  Match.objects.get(id=match_id)
    display_name = match.display_name()
    home_team = {
        "team": team_info(match.home_team.id),
        "lineup": lineup_info(match.id, home=True),
    }
    away_team = {
        "team": team_info(match.away_team.id),
        "lineup": lineup_info(match.id, home=False),
    }
    AceStreamFormSet = formset_factory(AceStreamForm)
    add_stream_formset = AceStreamFormSet()
    return render(request, 'games/templates/watch_game_2.html',
                  {"data": {
                      "is_mobile_tablet": _is_mobile,
                      "links": links,
                      "display_name": display_name,
                      "match": match,
                      "home_team": home_team,
                      "away_team": away_team,
                      "add_stream_formset": add_stream_formset,
                  }})

def get_match_info(request):
    _is_mobile = is_mobile(request)
    match_id = request.GET['match_id']
    match = Match.objects.get(id=match_id)
    streamable_game = StreamableMatch.objects.filter(match__id=match_id)
    links = []
    streamers = []
    link_count = 0
    if streamable_game:
        streamable_game = StreamableMatch.objects.get(match__id=match_id)
        links = Links.objects.get_links(streamable_game.scanned_match.id)
        streamers = links.distinct('streamer').values_list('streamer', flat=True)
        link_count = links.count()
    home_team = match.home_team.short_name
    away_team = match.away_team.short_name
    home_crest = match.home_team.crest
    away_crest = match.away_team.crest
    home_lineup = Lineup.objects.get_home_lineup(match_id)
    away_lineup = Lineup.objects.get_away_lineup(match_id)

    return render(request, 'games/templates/match_info.html',
                  {"data": {
                      "is_mobile_tablet": _is_mobile,
                      "match_id": match_id,
                      "home_team": home_team,
                      "away_team": away_team,
                      "home_crest": home_crest,
                      "away_crest": away_crest,
                      "home_lineup": home_lineup,
                      "away_lineup": away_lineup,
                      "streamers": ', '.join(streamers),
                      "link_count": link_count,
                  }})



# FORMS
@login_required
def add_ace_stream(request):
    links = []
    inserts = []
    ignored = []
    AceStreamFormSet = formset_factory(AceStreamForm)
    if request.method == 'POST':
        request_parameters = request.POST
        # print("Request Parameters: ")
        # print(request_parameters)

        form = AceStreamFormSet(request.POST)
        # print(form)

        if form.is_valid():
            # print(form.cleaned_data)
            for new_stream in form.cleaned_data:
                if('ace_stream' in new_stream):
                    streamable_match = StreamableMatch.objects.filter(match__id=request_parameters['match_id']).first()
                    if not streamable_match:
                        match = Match.objects.filter(id=request_parameters['match_id']).first()
                        # CREATE A SCANNED MATCH
                        scanned_match = ScannedMatch()
                        scanned_match.match = match.display_name()
                        scanned_match.time = str(match.match_date_time.time().hour) + str(match.match_date_time.time().minute) + ' GMT'
                        scanned_match.save()

                        # MAKE THE NEW SCANNED MATCH AS STREAMABLE
                        streamable_match = StreamableMatch()
                        streamable_match.scanned_match = scanned_match
                        streamable_match.match = match
                        streamable_match.save()

                    if new_stream['ace_stream'].startswith('acestream://') and len(new_stream['ace_stream'].lstrip('acestream://')) > 10:
                        # SAVE THE LINK
                        link = Links()
                        link.match = streamable_match.scanned_match
                        link.link = new_stream['ace_stream']
                        link.linkScore = 0
                        link.streamer = ''
                        link.save()

                        links.append(link.id)
                        inserts.append(new_stream['ace_stream'])

                    else:
                        ignored.append(new_stream['ace_stream'])

            new_links = serializers.serialize("json", Links.objects.filter(id__in=links).distinct('link'))

        return JsonResponse({
            "data": {
                "inserts": inserts,
                "ignored": ignored,
                "new_links": new_links,
            }
        })