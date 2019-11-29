from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from datetime import datetime, date

from bin.helper_scripts.makeRequest import make_request, request_headers

from leagues.models import League
from teams.models import Team, Teams_in_League

FOOTBALL_API_BASE_URL = "https://api.football-data.org/v2"
FOOTBALL_API_URLS = {
    "competitions": "/competitions/",
    "teams": "/teams/"
    }


def get_leagues():
    url = FOOTBALL_API_BASE_URL + FOOTBALL_API_URLS["competitions"]
    request = make_request(url, request_headers["football-api"])
    try:
        data = request["data"]
        for league in data["competitions"]:
            if league["plan"] == "TIER_ONE":
                try:
                    new_league = League.objects.get(
                        Q(api_id= league["id"]) | Q(name=league["name"])
                    )
                    if new_league and new_league.api_id is None:
                        new_league.api_id = league["id"]
                        new_league.save()
                except ObjectDoesNotExist:
                    print(league["name"] + " does not exists. Creating...")
                    new_league = League()
                    new_league.api_id = league["id"]
                    new_league.name = league["name"]
                    new_league.code = league["code"]
                    new_league.country = league["area"]["name"]
                    new_league.save()
                    print("Successfully created " + league["name"])

    except KeyError:
        print(request["message"])
        raise

    print("Leagues created/updated successfully!")
    return True


def get_teams():
    # Clear previous set leagues.
    # For example, a team might no longer be in the Champions league or the First division
    teams = Team.objects.all()
    for i in teams:
        i.leagues.clear()

    # Get new teams and update leagues on current teams only for the supported leagues
    tracked_leagues = League.objects.filter(tracked=True)
    for tracked_league in tracked_leagues:
        url = FOOTBALL_API_BASE_URL + \
              FOOTBALL_API_URLS["competitions"] + \
              str(tracked_league.api_id) + \
              FOOTBALL_API_URLS["teams"]

        request = make_request(url, request_headers["football-api"])
        try:
            data = request["data"]
            for team in data["teams"]:
                try:
                    new_team = Team.objects.get(api_id=team["id"])
                    if new_team:
                        new_team.leagues.add(League.objects.get(id=tracked_league.id))
                except ObjectDoesNotExist:
                    print(team["name"] + " does not exist. Creating...")
                    new_team = Team()
                    new_team.api_id = team["id"]
                    new_team.club_colors = team["clubColors"]
                    new_team.name = team["name"]
                    new_team.short_name = team["shortName"]
                    new_team.venue = team["venue"]
                    new_team.tla = team["tla"]
                    new_team.save()

                    # New team needs to exist before adding values to Many-to-Many field
                    new_team.leagues.add(League.objects.get(id=tracked_league.id))
                    print("Successfully created " + team["name"])
        except KeyError:
            print(request["message"])
            raise
    print("Teams created/updated successfully!")
    return True


def get_matches(date=date.today()):
    data = {}
    try:
        d = datetime.strftime(date, '%Y-%m-%d')
        url = "http://api.football-data.org/v2/matches?dateFrom=" + d + "&dateTo=" + d
        request = make_request(url, request_headers["football-api"])
        try:
            data = request['data']
        except KeyError:
            print(request['message'])
            raise
    except ValueError:
        raise ValueError('Invalid Date Format')

    return data
