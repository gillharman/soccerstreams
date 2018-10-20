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
    link_obj = {
        'link':""
    }

    requestUrl = str(urlString) + ".json"
    responseData = make_request(requestUrl)

    acestream_reg_ex = 'acestream://\w+'

    try:
        for dict in responseData:
            for child in dict['data']['children']:
                if child['kind'] == 't1':
                    regex_result = re.finditer(acestream_reg_ex, child['data']['body'])
                    for i in regex_result:
                        link_obj['link'] = i.group();
                        #body_html = child['data']['body_html']
                        #print(type(child['data']['body_html']))

                        ##wrap_ace_link = re.finditer(acestream_reg_ex, body_html)
                        #for j in wrap_ace_link:
                        #    print(j.group());
                        #    body_html.replace(j.group(), '&#x3C;a&#x3E;'+ j.group() +'&#x3C;/a&#x3E;')
                        #print(body_html)
                        # links_obj["body_html"] = Template(html.unescape(child['data']['body_html'])).render(
                        #     Context({"data": ""}))
                        #links_obj["body_html"] = Template(html.unescape(body_html).render(Context({"data": ""})))
                        #Could be multiple acestream link in one comment
                        # links = []
                        # for link in regex_result:
                        #     ace_link = {}
                        #     ace_link["link"] = link.group()
                        #     print('link.group: ' + link.group())
                        #     links.append(ace_link)
                        # links_obj["links"] = links
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