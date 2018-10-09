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

    dataObj = [];

    requestUrl = str(urlString) + ".json"
    responseData = make_request(requestUrl)

    acestream_reg_ex = 'acestream://\w+'

    try:
        for dict in responseData:
            for child in dict['data']['children']:
                if child['kind'] == 't1':
                    regex_result = re.finditer(acestream_reg_ex, child['data']['body'])
                    print(str(regex_result))
                    if regex_result is not None:
                        links_obj = {}
                        links_obj["kind"] = 'Ace'
                        links_obj["body_html"] = Template(html.unescape(child['data']['body_html'])).render(
                            Context({"data": ""}))
                        #Could be multiple acestream link in one comment
                        links = []
                        for link in regex_result:
                            ace_link = {}
                            ace_link["link"] = link.group()
                            links.append(ace_link)
                        links_obj["links"] = links
                        dataObj.append(links_obj)
                    else:
                        continue

    except KeyError:
        'Error. Unsuccessful connection...'

    if not dataObj:
        links = []
        ace_link = {}
        ace_link["link"]:""
        links.append(ace_link)
        links_obj = {
            "kind":"Post",
            "link":str(urlString),
            "body_html":"",
            "links": ace_link
        }
        dataObj.append(links_obj)

    return dataObj