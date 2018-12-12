import re

from .scanner_helper_functions import make_request, request_headers

from games.models import Game, Links

def start_scraper():
    new_games = scrape_games()
    # print(new_games)
    stored_games = store_game(new_games)
    new_links = scrape_ace_links(stored_games)
    l = store_links(new_links)
    return l

def store_game(arr):
    g = Game.objects.get_games().values_list('match', flat=True)
    for i in arr:
        if i["GameTitle"] not in g:
            game = Game();
            game.match = i["GameTitle"]
            game.postUrl = i["PostLink"]
            game.time = i["Time"]
            game.save()

    return Game.objects.get_games().values('id', 'postUrl')

def store_links(arr):
    print(arr)
    try:
        for i in arr:
            gameInstance = Game.objects.get(id=i["gameID"])
            if(gameInstance.aceLink == False) :
                gameInstance.aceLink = True
                gameInstance.save()
            link = Links()
            link.match = gameInstance
            link.streamer = i["author"]
            link.link = i["link"]
            link.linkScore = i["score"]
            link.save()

    except TypeError:
        print("Unable to save the game: " + TypeError)

def scrape_games():
    matches = []
    url = 'http://www.reddit.com/r/soccerstreams/.json'

    data = make_request(url, request_headers["reddit"])

    reg_ex = '(\[\d\d\:\d\d\s\D\D\D\])'

    try:
        for child in data['data']['children']:
            game_title_check = re.search(reg_ex, child['data']['title']) #Title with GMT Time ([00:00 GMT])
            if game_title_check:
                soccerMatch = {}
                soccerMatch["GameTitle"] = child['data']['title'].replace(game_title_check.group(), '').strip()
                soccerMatch["Time"] = game_title_check.group()[1:10]
                soccerMatch["PostLink"] = child['data']['url']
                matches.append(soccerMatch)
    except KeyError:
        'Error. Unsuccessful connection...'
    print(matches)
    return matches

def scrape_ace_links(arr):
    # print('Scraping ace links ' + arr);
    links = []

    for j in arr:
        urlString = j["postUrl"]

        requestUrl = str(urlString) + ".json"

        responseData = make_request(requestUrl, request_headers["reddit"])

        acestream_reg_ex = 'acestream://\w+'

        try:
            for dict in responseData:
                for child in dict['data']['children']:
                    if child['kind'] == 't1':
                        regex_result = re.finditer(acestream_reg_ex, child['data']['body'])
                        for i in regex_result:
                            link_obj = {}
                            link_obj['link'] = i.group();
                            link_obj['score'] = child['data']['score']
                            link_obj['author'] = child['data']['author']
                            link_obj['gameID'] = j["id"]
                            links.append(link_obj)
                    else:
                        continue

        except KeyError:
            'Error. Unsuccessful connection...'

    return links