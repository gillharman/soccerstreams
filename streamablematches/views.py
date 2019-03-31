from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.core import serializers

from .models import Links, StreamableMatch
from teams.models import Team_Logo
from matches.models import Match
from lineups.models import Lineup
from leagues.models import League
from bin.helper_scripts.isMobile import isMobile
from bin.helper_scripts.view_helpers import team_info, lineup_info

def welcome(request):
    return render(request, 'games/templates/welcome.html')

def home(request, league="PL"):
    is_mobile = isMobile(request)
    # games = Match.objects.get_games()
    games = Match.objects.filter(league__code=league).order_by('match_day')
    league_title = League.objects.get(code=league).name
    return render(request, 'games/templates/index.html',
                  {"data": {
                      "is_mobile_tablet": is_mobile,
                      "matches": games,
                      "league_title": league_title,
                  }})

def ajax_league_matches(request):
    league = request.GET['league']
    # print(league)
    is_mobile = isMobile(request)
    games = Match.objects.filter(league__code=league).order_by('match_day')
    return render(request, 'games/templates/league_matches.html',
                  {"data": {
                      "is_mobile_tablet": is_mobile,
                      "matches": games,
                  }})


def watch_game(request, match_id):
    is_mobile = isMobile(request)
    # streamable_game = StreamableMatch.objects.get(match__id=match_id)
    # links = Links.objects.get_links(streamable_game.scanned_match.id)
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
    return render(request, 'games/templates/watch_game_2.html',
                  {"data": {
                      "is_mobile_tablet": is_mobile,
                      # "links": links,
                      "display_name": display_name,
                      "match": match,
                      "home_team": home_team,
                      "away_team": away_team,
                  }})

def get_match_info(request):
    is_mobile = isMobile(request)
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
                      "is_mobile_tablet": is_mobile,
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