import re
import html

from django.template import Context, Template
from .scanner_helper_functions import make_request

def scan_for_games():
    dataObj = []
    #print("This runs", file=sys.stderr)
    url = 'http://www.reddit.com/r/soccerstreams/.json'

    data = make_request(url)

    reg_ex = '(\[\d\d\:\d\d\s\D\D\D\])'

    try:
        for child in data['data']['children']:
            game_title_check = re.search(reg_ex, child['data']['title']) #Title with GMT Time ([00:00 GMT])
            if game_title_check:
                game = {}
                game["GameTitle"] = child['data']['title'].replace(game_title_check.group(), '').strip()
                game["Time"] = game_title_check.group()[1:10]
                game["PostLink"] = child['data']['url']
                dataObj.append(game)
    except KeyError:
        'Error. Unsuccessful connection...'

    return dataObj

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