from bs4 import BeautifulSoup
import re
import difflib
from datetime import datetime, date

from matches.models import Match
from lineups.models import Lineup
from logs.models import RotowireRequest


def getMatchInstance(string, date_):
    matches = Match.objects.get_match_display_name()
    close_match = difflib.get_close_matches(string, matches, n=1)

    if close_match:
        m = Match.objects.get_match_from_display_name(close_match[0], date_)
        if m:
            return m.first()


def getLineup(tag):
    retVal = {
        'confirmed': False,
        'lineup': []
    }
    lineup_status = tag.find(class_=re.compile('lineup__status'))['class']
    if 'is-confirmed' in lineup_status:
        retVal['confirmed'] = True
    line = tag.find_all(class_=re.compile('lineup__player'))

    for l in line:
        player = {}
        pos = l.find(class_=re.compile('lineup__pos'))
        p = l.a.string
        player['position'] = pos.string
        player['name'] = p
        retVal['lineup'].append(player)
    return retVal


def saveLineup(o):
    if o['match']:
        existing_lineup = Lineup.objects.filter(match=o['match'], lineup_type=o['lineupType'])
        if existing_lineup:
            existing_lineup.delete()
        for player in o['lineup']:
            l = Lineup()
            l.position = player['position']
            l.lineup_type = o['lineupType']
            l.player = player['name']
            l.match = o['match']
            l.confirmed = o['confirmed']
            l.save()
    else:
        print('Skipping lineup for: ' + o['team'])
    return True


def storeLineups(league):
    html = ''
    raw_object = RotowireRequest.objects.get_(league)
    if raw_object:
        html = raw_object.html
    soup = BeautifulSoup(html)

    lineups = soup.find_all(class_=re.compile('lineup is-soccer'))
    for lineup in lineups:
        lineup_time = lineup.find(class_=re.compile('lineup__time')).stripped_strings
        date_ = datetime.strptime(list(lineup_time)[0] + ' ' + str(date.today().year), '%B %d %Y')
        matchup = lineup.find_all(class_=re.compile("lineup__mteam"))
        for m in matchup:
            if 'is-home' in m['class']:
                home_team = list(m.stripped_strings)[0]
            elif 'is-visit' in m['class']:
                away_team = list(m.stripped_strings)[0]
            else:
                print('Invalid match up')

        match = getMatchInstance(home_team + ' vs ' + away_team, date_.date())
        # print('match ' + match)
        home_lineup = getLineup(lineup.find(class_='lineup__list is-home'))
        away_lineup = getLineup(lineup.find(class_='lineup__list is-visit'))

        saved_home_lineup = saveLineup({
            'match': match,
            'confirmed': home_lineup['confirmed'],
            'lineup': home_lineup['lineup'],
            'lineupType': 'H',
            'team': home_team
        })
        saved_away_lineup = saveLineup({
            'match': match,
            'confirmed': away_lineup['confirmed'],
            'lineup': away_lineup['lineup'],
            'lineupType': 'A',
            'team': away_team
        })
    return True

def start():
    LEAGUES = ["PL", "CL", "FL1", "BL1", "SA", "DED", "PPL", "PD"]
    for league in LEAGUES:
        storeLineups(league)