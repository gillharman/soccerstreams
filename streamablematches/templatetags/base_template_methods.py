from django import template

register = template.Library()


@register.filter(name="has_avatar")
def has_avatar(user):
    return hasattr(user, 'useravatar')