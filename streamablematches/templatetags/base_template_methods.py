from django import template

from bin.helper_scripts.storage import AvatarFileRetrieval

from users.models import UserAvatar

register = template.Library()


@register.filter(name="get_avatar_instance")
def get_avatar_instance(user):
    avatar_instance = ""
    try:
        avatar_instance = AvatarFileRetrieval(user).getavatarinstance()
    except UserAvatar.DoesNotExist:
        pass
    return avatar_instance


@register.filter(name="get_avatar")
def get_avatar(user):
    avatar_bytes = ""
    try:
        avatar = AvatarFileRetrieval(user)
        avatar_bytes = avatar.getb64encodedimage()
        avatar_bytes = str(avatar_bytes)[2:-1]  # Removes [b']......[']
    except UserAvatar.DoesNotExist:
        pass

    return avatar_bytes
