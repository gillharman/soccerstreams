from django.shortcuts import render

from bin.scanner.scanner import scrape_ace_links
from .models import Game, Links


def welcome(request):
    return render(request, 'games/welcome.html')

def matches(request):
    games = Game.objects.get_games()
    # games = []
    return render(request, 'games/games.html',
                  {"matches" : games})

def watch_game(request):
    responseData = request.POST
    selected_game_links = Links.objects.get_links(responseData['match-id'])
    print(selected_game_links)
    selected_game = responseData['match-title']
    return render(request, 'games/watch_game.html',
                  {"data": {"links" : selected_game_links, "selected_game" : selected_game}})