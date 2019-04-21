from django import template
from datetime import date, datetime
import random

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
        r = 'Today'
    else:
        r = datetime.strftime(value, "%m/%d")
    return r

@register.filter(name="time_format")
def time_format(value):
    n = random.randint(1,3)
    match_date = value.date()
    today_day = date.today()
    # if match_date >= today_day:
    if n == 3:
        r = datetime.strftime(value, "%I:%M %p")
    else:
        r = ''
    return r


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



# HELPER FUNCTION FOR THE TAGS ABOVE
def get_logo_url(team_id, logo_dimension):
    try:
        return Team.objects.get(id=team_id).get_logo_url(dimension=logo_dimension)
    except:
        return ""