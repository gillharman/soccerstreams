from bs4 import BeautifulSoup, SoupStrainer
from bin.helper_scripts.makeRequest import make_request, request_headers

from logs.models import RotowireRequest
from leagues.models import League

LEAGUES = ["PL", "CL", "FL1", "BL1", "SA", "DED", "PPL", "PD"]

ROTOWIRE_LEAGUE_URLS = {
    "PL": "",
    "FL1": "?league=FRAN",
    "PD": "?league=LIGA",
    "SA": "?league=SERI",
    "BL1": "?league=BUND",
    "MLS": "?league=MLS",
    "CL": "?league=UCL",
    "LMX": "?league=LMX"
}

def getLineups():
    for league in LEAGUES:
        rotowire_url = "https://www.rotowire.com/soccer/lineups.php"
        if league in ROTOWIRE_LEAGUE_URLS:
            rotowire_url += ROTOWIRE_LEAGUE_URLS[league]
        else:
            continue
        rotowire_html = make_request(rotowire_url, request_headers['rotowire'], 'text')
        lineup_html = BeautifulSoup(rotowire_html['data'], parse_only=SoupStrainer(class_="lineups"), features="html.parser")

        #ONLY GET NEW LINEUP IF IT CHANGED
        current_html = RotowireRequest.objects.get_html(league)
        if current_html:
            current_html = current_html.html
        else:
            current_html = ''
        if current_html != str(lineup_html):
            rr = RotowireRequest()
            rr.html = str(lineup_html)
            rr.league = League.objects.get(code=league)
            rr.save()
    return True
