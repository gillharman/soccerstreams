import re

from bin.helper_scripts.makeRequest import make_request, request_headers

from streamablematches.models import ScannedMatch, Links

def start():
    new_games = scrape_games()
    # print(new_games)
    stored_games = store_game(new_games)
    new_links = scrape_ace_links(stored_games)
    l = store_links(new_links)
    return l

def store_game(arr):
    g = ScannedMatch.objects.get_games().values_list('match', flat=True)
    for i in arr:
        ### CHECK IF MATCH EXISTS BEFORE INSERT ###
        if i["GameTitle"] not in g:
            game = ScannedMatch();
            game.match = i["GameTitle"]
            game.postUrl = i["PostLink"]
            game.time = i["Time"]
            game.save()

    return ScannedMatch.objects.get_games().values('id', 'postUrl')

def store_links(arr):
    # print(arr)
    try:
        for i in arr:
            # ONLY SAVE NEW LINKS
            if not Links.objects.filter(link=i["link"], id=i["gameID"], streamer=i["author"]):
                gameInstance = ScannedMatch.objects.get(id=i["gameID"])
                if(gameInstance.aceLink == False) :
                    gameInstance.aceLink = True
                    gameInstance.save()
                link = Links()
                link.match = gameInstance
                link.streamer = i["author"]
                link.link = i["link"]
                link.linkScore = i["score"]
                link.save()
            else:
                print(i["link"] + ' already exits for game_id=' + i["gameID"])

    except Exception as e:
        print('An error occurred: ' + repr(e))

def scrape_games():
    matches = []
    url = 'http://www.reddit.com/r/soccerstreams/.json'
    request = make_request(url, request_headers["reddit"])
    data = ''
    try:
        if request['data']:
            data = request['data']
    except Exception as e:
        print('An error occurred when scraping for games ' + request['message'])
        raise

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
    except Exception as e:
        print('An error occurred: ' + repr(e))
    return matches

def scrape_ace_links(arr):
    # print('Scraping ace links ' + arr);
    links = []

    for j in arr:
        urlString = j["postUrl"]

        requestUrl = str(urlString) + ".json"

        request = make_request(requestUrl, request_headers["reddit"])

        data = ''
        try:
            if request['data']:
                data = request['data']
        except Exception as e:
            print('An error occurred when scraping for links ' + request['message'])
            raise

        acestream_reg_ex = 'acestream://\w+'

        try:
            for dict in data:
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


        except Exception as e:
            print('An error occurred: ' + repr(e))

    return links