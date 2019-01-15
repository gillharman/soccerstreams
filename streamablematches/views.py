from django.shortcuts import render

from .models import Links, StreamableMatch
from matches.models import Match
from lineups.models import Lineup
from bin.helper_scripts.isMobile import isMobile

def welcome(request):
    return render(request, 'games/templates/welcome.html')

def matches(request):
    is_mobile = isMobile(request)
    games = Match.objects.get_games()
    return render(request, 'games/templates/games.html',
                  {"data" : {
                      "is_mobile_tablet": is_mobile,
                      "matches": games,
                  }})

def watch_game(request, match_id):
    is_mobile = isMobile(request)
    streamable_game = StreamableMatch.objects.get(match__id=match_id)
    links = Links.objects.get_links(streamable_game.scanned_match.id)
    selected_game = Match.objects.get(id=match_id).display_name()
    return render(request, 'games/templates/watch_game.html',
                  {"data": {
                      "is_mobile_tablet": is_mobile,
                      "links": links,
                      "selected_game": selected_game
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