from django.shortcuts import render

from .models import Game, Links
from bin.is_mobile import isMobile

def welcome(request):
    return render(request, 'games/welcome.html')

def matches(request):
    is_mobile = isMobile(request)
    games = Game.objects.get_games()
    return render(request, 'games/games.html',
                  {"data" : {
                      "matches": games,
                      "is_mobile_tablet": is_mobile,
                  }})

def watch_game(request, match_id):
    selected_game_links = Links.objects.get_links(match_id)
    game_streamers = Links.objects.get_streamers(match_id)
    selected_game = Game.objects.get_match_name(match_id)
    return render(request, 'games/watch_game.html',
                  {"data": {
                      "streamers": game_streamers,
                      "links": selected_game_links,
                      "selected_game": selected_game
                  }})

def get_match_info(request):
    is_mobile = isMobile(request)
    match_id = request.GET['match_id']
    name = Game.objects.get_match_name(match_id)
    game_links = Links.objects.get_links(match_id)
    streamers = game_links.distinct('streamer').values_list('streamer', flat=True)
    link_count = game_links.count()
    home_crest = "http://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg"
    away_crest = "http://upload.wikimedia.org/wikipedia/de/5/5c/Chelsea_crest.svg"

    return render(request, 'games/match_info.html',
                  {"data": {
                      "name": name,
                      "match_id": match_id,
                      "home_crest": home_crest,
                      "away_crest": away_crest,
                      "streamers": ', '.join(streamers),
                      "link_count": link_count,
                      "is_mobile_tablet": is_mobile,
                  }})