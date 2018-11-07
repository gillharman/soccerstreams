import re

from .scanner_helper_functions import make_request

from games.models import Game, Links

def store_game(obj):
    game = Game();
    game.match = obj["GameTitle"]
    game.url = obj["PostLink"]
    game.time = obj["Time"]
    game.save()

def scan_for_games():
    dataObj = []
    url = 'http://www.reddit.com/r/soccerstreams/.json'

    data = make_request(url)

    reg_ex = '(\[\d\d\:\d\d\s\D\D\D\])'

    try:
        for child in data['data']['children']:
            game_title_check = re.search(reg_ex, child['data']['title']) #Title with GMT Time ([00:00 GMT])
            if game_title_check:
                soccerMatch = {}
                soccerMatch["GameTitle"] = child['data']['title'].replace(game_title_check.group(), '').strip()
                soccerMatch["Time"] = game_title_check.group()[1:10]
                soccerMatch["PostLink"] = child['data']['url']
                store_game(soccerMatch)
                # dataObj.append(soccerMatch)
    except KeyError:
        'Error. Unsuccessful connection...'

    # return dataObj

def scan_acestream_link(urlString):

    links = []

    requestUrl = str(urlString) + ".json"
    responseData = make_request(requestUrl)

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
                        links.append(link_obj)
                else:
                    continue

    except KeyError:
        'Error. Unsuccessful connection...'

    retVal = {}
    if links:
        retVal['type'] = "ACESTREAM"
        retVal['links'] = links
    else:
        retVal['type'] = "FULL_THREAD"
        retVal['links'] = str(urlString)

    return retVal