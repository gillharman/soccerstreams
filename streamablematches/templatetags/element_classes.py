from django import template
from datetime import date, datetime
import random

from bin.helper_scripts.linkClassClassifier import link_class_classifier

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