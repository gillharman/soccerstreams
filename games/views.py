from django.shortcuts import render
from .models import Game, Links


def welcome(request):
    return render(request, 'games/welcome.html')

def matches(request):
    games = Game.objects.get_games()
    return render(request, 'games/games.html',
                  {"matches" : games})

def watch_game(request, match_id):
    selected_game_links = Links.objects.get_links(match_id)
    # print(selected_game_links)
    selected_game = Game.objects.get_match_name(match_id)
    return render(request, 'games/watch_game.html',
                  {"data": {"links" : selected_game_links, "selected_game" : selected_game}})