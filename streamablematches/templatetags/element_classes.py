from django import template

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
