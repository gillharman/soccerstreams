from datetime import datetime
import pytz

from leagues.models import League
from teams.models import Team
from matches.models import Match


def sanitize_string(string, delimiter='_'):
    words = string.split(delimiter)
    capitalized_words = []
    for word in words:
        capitalized_words.append(word.capitalize())
    return ' '.join(capitalized_words)


def store_matches(data):
    retVal = {}
    tracked_leagues = League.objects.all().values_list('name', flat=True)
    statuses = dict((key,value) for (value,key) in Match.STATUS_CHOICES)
    ignore = 0
    insert = 0
    update = 0
    try:
        for i in data['matches']:
            # SANITIZE STATUS
            status = sanitize_string(i["status"])

            # IGNORE - IF LEAGUE IS NOT TRACKED
            if i["competition"]["name"] not in tracked_leagues:
                ignore += 1
                # print('Match for ' + i["competition"]["name"] + ' are not tracked')
                continue
            # UPDATE - PREEXISTING
            elif Match.objects.filter(api_match_id=i["id"]):
                m = Match.objects.get(api_match_id=i["id"])
                m.status = statuses[status]
                m.save()
                update += 1
            # INSERT - NEW MATCHES
            else:
                m = Match()
                m.api_match_id = i["id"]
                m.status = statuses[status]
                m.match_day = i["matchday"]
                mdt = datetime.strptime(i["utcDate"], '%Y-%m-%dT%H:%M:%SZ')
                mdt = mdt.replace(tzinfo=pytz.utc)  ### SET TIMEZONE
                m.match_date_time = mdt
                m.home_team = Team.objects.get(api_id=i["homeTeam"]["id"])
                m.away_team = Team.objects.get(api_id=i["awayTeam"]["id"])
                m.league = League.objects.get(name=i["competition"]["name"])
                m.save()
                insert += 1
    except KeyError:
        raise
    retVal['insert'] = str(insert)
    retVal['update'] = str(update)
    retVal['ignore'] = str(ignore)

    return retVal