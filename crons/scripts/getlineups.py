from bs4 import BeautifulSoup
from bs4.element import SoupStrainer

from utils import make_request

from logs.models import RotowireRequest
from leagues.models import League

from soccerstreams.settings import base as settings

LEAGUES = ["PL", "CL", "FL1", "BL1", "SA", "DED", "PPL", "PD"]


def get_lineups():
    for league in LEAGUES:
        if league in settings.ROTOWIRE_LEAGUE_URLS:
            url = settings.ROTOWIRE_BASE_URL + settings.ROTOWIRE_LEAGUE_URLS[league]
        else:
            continue
        rotowire_html = make_request(url, settings.REQUEST_HEADERS['rotowire'], 'text')
        lineup_html = BeautifulSoup(rotowire_html['data'], parse_only=SoupStrainer(class_="lineups"), features="html.parser")

        # ONLY GET NEW LINEUP IF IT CHANGED
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
