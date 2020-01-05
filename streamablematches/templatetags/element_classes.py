from django import template
from datetime import date, datetime
from pytz import timezone

from bin.helper_scripts.linkClassClassifier import link_class_classifier

from teams.models import Team

register = template.Library()


@register.filter(name="link_score_class")
def link_score_class(value):
    classes = ['success', 'danger', 'secondary']
    return link_class_classifier(value, classes)


@register.filter(name="link_score_icon_class")
def link_score_icon_class(value):
    classes = ['fa-arrow-circle-o-up', 'fa-arrow-circle-o-down', 'fa fa-star-o']
    return link_class_classifier(value, classes)


@register.filter(name="date_format")
def date_format(value):
    match_date = value.date()
    today_day = date.today()
    if match_date == today_day:
        d = 'Today'
    else:
        day = datetime.strftime(value, "%a, ")
        date_of_month = datetime.strftime(value, "%m/%d")
        if date_of_month.startswith("0"):
            date_of_month = date_of_month[1:]
        d = day + date_of_month

    return d


@register.filter(name="time_format")
def time_format(value):
    eastern = timezone("US/Eastern")
    eastern_time = value.astimezone(eastern)
    t = datetime.strftime(eastern_time, "%I:%M %p")
    if t.startswith("0"):
        t = t[1:]

    return t


@register.filter(name="get_status_class")
def get_status_class(match):
    element_class = ""
    if match.status == match.FINISHED:
        element_class = "full-time"

    return element_class


@register.filter(name="get_result")
def get_result(match, side):
    result = ""
    if match.status == match.FINISHED:
        if match.winner == match.HOME_TEAM:
            if side == "home":
                result = "winner"
            else:
                result = "loser"

        elif match.winner == match.AWAY_TEAM:
            if side == "home":
                result = "loser"
            else:
                result = "winner"

        elif match.winner == match.DRAW:
            result = "draw"

    return result


@register.filter(name="get_logo_url_48x48")
def get_logo_url_48x48(team_id):
    return get_logo_url(team_id, 48)


@register.filter(name="get_logo_url_96x96")
def get_logo_url_96x96(team_id):
    return get_logo_url(team_id, 96)


@register.filter(name="right_border")
def right_border(value):
    if (value % 2) == 1:  # LEFT SIDE COLUMN - APPLY RIGHT BORDER
        return " right-border"
    else:
        return ""


@register.filter(name="bottom_border")
def bottom_border(value, num_matches):
    last_border_applicable_row = num_matches - 2
    if num_matches % 2 == 1:  # IF ODD NUMBER OF MATCHES -- BORDER IS APPLICABLE ON THE SECOND TO LAST MATCH
        last_border_applicable_row = num_matches - 1

    if value <= last_border_applicable_row:
        return " bottom-border"
    else:
        return ""


@register.filter(name="get_league_homepage_url")
def get_league_homepage_url(league_code):
    if league_code == 'PL':
        return '/'
    else:
        return '/' + str(league_code)


@register.filter(name="has_errors")
def has_errors(form):
    if form.errors:
        return "display: block;"
    else:
        return ""


# HELPER FUNCTION FOR THE TAGS ABOVE
def get_logo_url(team_id, logo_dimension):
    try:
        return Team.objects.get(id=team_id).get_logo_url(dimension=logo_dimension)
    except:
        return ""