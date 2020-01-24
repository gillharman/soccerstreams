from django.db.models import Q
from calendar import monthrange
from datetime import datetime
import pytz

from utils import make_request, sanitize_string

from leagues.models import League
from teams.models import Team
from matches.models import Match

from soccerstreams import settings as settings


def get_leagues():
    url = settings.FOOTBALL_API_BASE_URL + settings.FOOTBALL_API_URLS["competitions"]
    request = make_request(url, settings.REQUEST_HEADERS["footballApi"])
    try:
        data = request["data"]
        for league in data["competitions"]:
            if league["plan"] == "TIER_ONE":
                try:
                    new_league = League.objects.get(
                        Q(api_id=league["id"]) | Q(name=league["name"])
                    )
                    if new_league and new_league.api_id is None:
                        new_league.api_id = league["id"]
                        new_league.save()
                except League.DoesNotExist:
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
        url = settings.FOOTBALL_API_BASE_URL + settings.FOOTBALL_API_URLS["teams"] % str(tracked_league.api_id)
        request = make_request(url, settings.REQUEST_HEADERS["footballApi"])
        try:
            data = request["data"]
            for team in data["teams"]:
                try:
                    new_team = Team.objects.get(api_id=team["id"])
                    if new_team:
                        new_team.leagues.add(League.objects.get(id=tracked_league.id))
                except Team.DoesNotExist:
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


def get_matches(start_date=None, end_date=None):
    today = datetime.today()
    last_day_of_month = monthrange(today.year, today.month)[1]  # Returns tuple Ex. (3, 31)
    if start_date is None:
        start_date = datetime(today.year, today.month, 1)
    if end_date is None:
        end_date = datetime(today.year, today.month, last_day_of_month)

    try:
        start_date = datetime.strftime(start_date, '%Y-%m-%d')
        end_date = datetime.strftime(end_date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Invalid Date Format!")

    query = "?dateFrom=%s&dateTo=%s" % (start_date, end_date)
    tracked_leagues = League.objects.filter(tracked=True)
    match_status_choices = dict((key, value) for (value, key) in Match.STATUS_CHOICES)
    match_winner_choices = dict((key, value) for (value, key) in Match.WINNER_CHOICES)
    for tracked_league in tracked_leagues:
        url = settings.FOOTBALL_API_BASE_URL + settings.FOOTBALL_API_URLS["matches"] % str(tracked_league.api_id) + query
        request = make_request(url, settings.REQUEST_HEADERS["footballApi"])
        try:
            data = request["data"]
            for match in data["matches"]:
                try:
                    home_team = Team.objects.get(api_id=match["homeTeam"]["id"])
                    away_team = Team.objects.get(api_id=match["awayTeam"]["id"])
                    match_status = sanitize_string(match["status"], delimiter="_")  # Ex. IN_PLAY -> In Play
                    match_winner = sanitize_string(match["score"]["winner"], delimiter="_")
                    match_datetime = datetime.strptime(match["utcDate"], "%Y-%m-%dT%H:%M:%SZ")
                    match_datetime = match_datetime.replace(tzinfo=pytz.utc)
                    new_match = Match()
                    try:
                        new_match = Match.objects.get(api_match_id=match["id"])
                    except Match.DoesNotExist as e:
                        print(match["homeTeam"]["name"] +
                              " vs " + match["awayTeam"]["name"] +
                              " does not exist. Creating...")
                        new_match.api_match_id = match["id"]
                        new_match.match_day = match["matchday"]
                        new_match.match_date_time = match_datetime
                        new_match.home_team = home_team
                        new_match.away_team = away_team
                        new_match.league = League.objects.get(id=tracked_league.id)
                    finally:
                        new_match.status = match_status_choices[match_status]
                        new_match.goals_scored_home_team = match["score"]["fullTime"]["homeTeam"]
                        new_match.goals_scored_away_team = match["score"]["fullTime"]["awayTeam"]
                        new_match.penalty_goals_home_team = match["score"]["penalties"]["homeTeam"]
                        new_match.penalty_goals_away_team = match["score"]["penalties"]["awayTeam"]
                        if match_winner is not None and match_winner != "":
                            new_match.winner = match_winner_choices[match_winner]
                        new_match.save()
                except Team.DoesNotExist as e:
                    print("Home or Away does not exists...")
                    raise
                except KeyError:
                    raise
                except ValueError:
                    raise ValueError("Invalid Date Format!")
        except KeyError:
            print(request["message"])
            raise
    print("Matches created/updated successfully!")

    return True


def update_match_day():
    leagues = League.objects.filter(tracked=True)
    for league in leagues:
        url = settings.FOOTBALL_API_BASE_URL + settings.FOOTBALL_API_URLS["competitionSeasons"] % str(league.api_id)
        request = make_request(url, settings.REQUEST_HEADERS["footballApi"])
        try:
            data = request["data"]
            try:

                league.current_match_day = data["currentSeason"]["currentMatchday"]
                league.save()
            except KeyError as e:
                print(e)
        except KeyError as e:
            print("{0} KeyError - {1}".format(str(request["message"]), e.__str__()))

    return True
