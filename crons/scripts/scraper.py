import re

from utils import make_request

from streamablematches.models import ScannedMatch, Link

from soccerstreams import settings as settings


def start():
    new_games = scrape_games()
    # print(new_games)
    stored_games = store_game(new_games)
    new_links = scrape_ace_links(stored_games)
    stored_links = store_links(new_links)

    return stored_links


def store_game(arr):
    g = ScannedMatch.objects.get_games().values_list('match', flat=True)
    for i in arr:
        # CHECK IF MATCH EXISTS BEFORE INSERT
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
            if not Link.objects.filter(link=i["link"], id=i["gameID"], streamer=i["author"]):
                gameInstance = ScannedMatch.objects.get(id=i["gameID"])
                if (gameInstance.aceLink == False):
                    gameInstance.aceLink = True
                    gameInstance.save()
                link = Link()
                link.match = gameInstance
                link.streamer = i["author"]
                link.link = i["link"]
                link.linkScore = i["score"]
                link.save()
            else:
                print(i["link"] + ' already exits for game_id=' + i["gameID"])

    except Exception as e:
        print('An error occurred: ' + repr(e))

    return True


def scrape_games():
    matches = []
    url = settings.REDDIT_BASE_URL + settings.REDDIT_API_URL["soccerstreams"]
    request = make_request(url, settings.REQUEST_HEADERS["reddit"])
    data = ''
    try:
        if request['data']:
            data = request['data']
    except Exception as e:
        print('An error occurred when scraping for games: ' + request['message'])
        raise

    reg_ex = "(\[\d\d\:\d\d\s\D\D\D\])"

    try:
        for child in data['data']['children']:
            game_title_check = re.search(reg_ex, child['data']['title'])  # Title with GMT Time ([00:00 GMT])
            if game_title_check:
                soccer_match = {
                    "GameTitle": child['data']['title'].replace(game_title_check.group(), '').strip(),
                    "Time": game_title_check.group()[1:10],
                    "PostLink": child['data']['url']
                }
                matches.append(soccer_match)
    except Exception as e:
        print('An error occurred: ' + repr(e))

    return matches


def scrape_ace_links(arr):
    # print('Scraping ace links ' + arr);
    links = []

    for j in arr:
        url_string = j["postUrl"]

        request_url = str(url_string) + ".json"

        request = make_request(request_url, settings.REQUEST_HEADERS["reddit"])

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
                            link_obj = {
                                "link": i.group(),
                                "score": child['data']['score'],
                                "author": child['data']['author'],
                                "gameID": j["id"]
                            }
                            links.append(link_obj)
                    else:
                        continue

        except Exception as e:
            print('An error occurred: ' + repr(e))

    return links
