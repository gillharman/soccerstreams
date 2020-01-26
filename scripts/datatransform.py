import os
import json

from streamablematches.models import League, Team, Teams_in_League, Team_Logo


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
        # CHECK IF TEAM ALREADY EXITS
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

    print('Team Transform: Total inserts: ' + str(insert))
    print('Team Transform: Ignored: ' + str(ignore))


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

    print('Team in Leagues Transform: Total inserts: ' + str(insert))
    print('Team in Leagues Transform: Ignored: ' + str(ignore))


def transform():
    os.chdir('data')
    for filename in os.listdir():
        if filename not in 'leagues.txt':
            with open(filename) as f:
                data = json.load(f)
                transform_teams(data)
                transform_teams_in_league(data)


def transform_logos(data):
    for logo in data:
        team = Team.objects.filter(api_id=logo["team__api_id"]).first()
        if team:
            current = Team_Logo.objects.filter(team=team).first()
            if current:
                print('Logo Already exists in database for ' + current.team.name)
            else:
                print('Creating new Logo entry for ' + team.name)
                team_logo = Team_Logo()
                team_logo.logo_48x48 = logo["logo_48x48"]
                team_logo.logo_48x48_url = logo["logo_48x48_url"]
                team_logo.logo_96x96 = logo["logo_96x96"]
                team_logo.logo_96x96_url = logo["logo_96x96_url"]
                team_logo.team = team
                team_logo.save()


def update_logos(data):
    updated = 0
    ignored = 0
    for logo in data:
        team_logo = Team_Logo.objects.filter(team__api_id=logo["team__api_id"]).first()
        if team_logo:
            team_logo.logo_48x48 = logo["logo_48x48"]
            team_logo.logo_48x48_url = logo["logo_48x48_url"]
            team_logo.logo_96x96 = logo["logo_96x96"]
            team_logo.logo_96x96_url = logo["logo_96x96_url"]
            team_logo.save()

            updated += 1
        else:
            ignored += 1


def read_file():
    path = input("Path of the file: ")
    json_object = input("Load into json object? (Y/N) ")
    with open(path, "r") as f:
        if json_object.lower() == "y":
            data = json.load(f)
        else:
            data = f.read()

    return data
