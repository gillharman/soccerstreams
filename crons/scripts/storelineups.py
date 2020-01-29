from bs4 import BeautifulSoup
import re
import difflib
from datetime import datetime, date

from streamablematches.models.competitions import MatchCopy, LineupCopy
from streamablematches.models.logs import RotowireRequestLog


def get_match_instance(string, date_):
    matches = MatchCopy.objects.get_match_display_name()
    close_match = difflib.get_close_matches(string, matches, n=1)

    if close_match:
        m = MatchCopy.objects.get_match_from_display_name(close_match[0], date_)
        # print(m)
        if m:
            # print(m.first().display_name())
            return m.first()


def get_lineup(tag):
    ret_val = {
        'confirmed': False,
        'lineup': []
    }
    lineup_status = tag.find(class_=re.compile('lineup__status'))['class']
    if 'is-confirmed' in lineup_status:
        ret_val['confirmed'] = True
    line = tag.find_all(class_=re.compile('lineup__player'))

    for l in line:
        player = {}
        pos = l.find(class_=re.compile('lineup__pos'))
        p = l.a.string
        player['position'] = pos.string
        player['name'] = p
        ret_val['lineup'].append(player)
    return ret_val


def save_lineup(o):
    ret_val = {"update":0, "insert":0}
    existing_lineup = LineupCopy.objects.filter(match=o['match'], lineup_type=o['lineupType'])
    if existing_lineup:
        ret_val['update'] += 1
        existing_lineup.delete()
    for player in o['lineup']:
        l = LineupCopy()
        l.position = player['position']
        l.lineup_type = o['lineupType']
        l.player = player['name']
        l.match = o['match']
        l.confirmed = o['confirmed']
        l.save()
    return ret_val


def store_lineups(league):
    lineup_html = ''
    html = RotowireRequestLog.objects.get_html(league)
    if html and html.parsed_count == 0:
        lineup_html = html.html
    soup = BeautifulSoup(lineup_html, features="html.parser")

    if soup.contents:
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

            match = get_match_instance(home_team + ' vs ' + away_team, date_.date())
            # print('match ' + match)
            home_lineup = get_lineup(lineup.find(class_='lineup__list is-home'))
            away_lineup = get_lineup(lineup.find(class_='lineup__list is-visit'))

            if match:
                saved_home_lineup = save_lineup({
                    'match': match,
                    'confirmed': home_lineup['confirmed'],
                    'lineup': home_lineup['lineup'],
                    'lineupType': 'H',
                    'team': home_team
                })
                saved_away_lineup = save_lineup({
                    'match': match,
                    'confirmed': away_lineup['confirmed'],
                    'lineup': away_lineup['lineup'],
                    'lineupType': 'A',
                    'team': away_team
                })
                if saved_away_lineup['update'] == 1:
                    print(home_team + ' vs ' + away_team + ' updated.')
                else:
                    print(home_team + ' vs ' + away_team + ' added.')
            else:
                print(home_team + ' vs ' + away_team + ' skipped.')
        html.parsed_count += 1
        html.save()
    else:
        print('No new or updated lineup information is available for ' + league)


def start():
    LEAGUES = ["PL", "CL", "FL1", "BL1", "SA", "DED", "PPL", "PD"]
    for league in LEAGUES:
        store_lineups(league)
    return 'Complete'
