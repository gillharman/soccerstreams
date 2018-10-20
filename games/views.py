from django.shortcuts import render
from .scanner.scanner import scan_for_games, scan_acestream_link
from .models import Game

def welcome(request):
    return render(request, 'games/welcome.html')

def matches(request):
    games = scan_for_games()
    return render(request, 'games/games.html',
                  {"matches" : games})

def watch_game(request):
    responseData = request.POST

    ##For Testing Purpose##
    # selected_game = "Test"
    # data = scan_acestream_link("https://www.reddit.com/r/soccerstreams/comments/9c3g4s/1630_gmt_manchester_city_vs_newcastle_united/.json")


    data = scan_acestream_link(responseData['match-post-link'])
    print(data)
    selected_game = responseData['match-title']
    #print(ace_links[0]["body_html"])
    return render(request, 'games/watch_game.html',
                  {"data": {"link_type": data['type'], "links" : data['links'], "selected_game" : selected_game}})