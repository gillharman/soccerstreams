import os
import json

from leagues.models import League
from teams.models import Team, Teams_in_League

def transform_leagues(data):
    for i in data['competitions']:
        league = League()
        league.name = i["name"]
        league.code = i["code"]
        league.country = i["area"]["name"]
        league.save()


def transform_teams(data):
    ignore = 0
    insert = 0
    for i in data['teams']:
        ### CHECK IF TEAM ALREADY EXITS ###
        if Team.objects.filter(api_id=i['id'], name=i['name']):
            ignore += 1
            print(i['name'] + ' already exists')
        else:
            team = Team()
            team.api_id = i['id']
            team.name = i['name']
            team.short_name = i['shortName']
            team.tla = i['tla']
            team.venue = i['venue']
            team.club_colors = i['clubColors']
            team.crest = i['crestUrl']
            team.save()
            insert += 1

    print('Total inserts: ' + str(insert))
    print('Ignored: ' + str(ignore))

def transform_teams_in_league(data):
    ignore = 0
    insert = 0
    league = League.objects.get(code=data['competition']['code'])
    for i in data['teams']:
        team = Team.objects.get(api_id=i['id'], name=i['name'])
        if Teams_in_League.objects.filter(team=team, league=league):
            print(team.name + ' already exists in this competition')
            ignore += 1
        else:
            league_team = Teams_in_League()
            league_team.team = team
            league_team.league = league
            league_team.save()
            insert += 1

    print('Total inserts: ' + str(insert))
    print('Ignored: ' + str(ignore))


def transform():
    os.chdir('data')
    for filename in os.listdir():
        if filename not in 'leagues.txt':
            with open(filename) as f:
                data = json.load(f)
                transform_teams(data)
                transform_teams_in_league(data)