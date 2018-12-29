from django.shortcuts import render
# from django.http import JsonResponse
# from datetime import date

from .models import ScannedMatch, Links
from teams.models import Team
from bin.helper_scripts.isMobile import isMobile
# from bin.helper_scripts.makeRequest import make_request, request_headers

def welcome(request):
    return render(request, 'games/templates/welcome.html')

def matches(request):
    is_mobile = isMobile(request)
    games = ScannedMatch.objects.get_games()
    return render(request, 'games/templates/games.html',
                  {"data" : {
                      "is_mobile_tablet": is_mobile,
                      "matches": games,
                  }})

def watch_game(request, match_id):
    is_mobile = isMobile(request)
    links = Links.objects.get_links(match_id)
    selected_game = ScannedMatch.objects.get_match_name(match_id)
    return render(request, 'games/templates/watch_game.html',
                  {"data": {
                      "is_mobile_tablet": is_mobile,
                      "links": links,
                      "selected_game": selected_game
                  }})

def get_match_info(request):
    home_team = ''
    away_team = ''
    is_mobile = isMobile(request)
    match_id = request.GET['match_id']
    name = ScannedMatch.objects.get_match_name(match_id)
    game_links = Links.objects.get_links(match_id)
    streamers = game_links.distinct('streamer').values_list('streamer', flat=True)
    link_count = game_links.count()
    home_crest = "http://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg"
    away_crest = "http://upload.wikimedia.org/wikipedia/de/5/5c/Chelsea_crest.svg"

    return render(request, 'games/templates/match_info.html',
                  {"data": {
                      "is_mobile_tablet": is_mobile,
                      "name": name,
                      "match_id": match_id,
                      "home_crest": home_crest,
                      "away_crest": away_crest,
                      "streamers": ', '.join(streamers),
                      "link_count": link_count,
                  }})