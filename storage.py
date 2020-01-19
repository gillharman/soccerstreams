from io import BytesIO
from base64 import b64encode
from PIL import Image

from users.models import UserAvatar


class AvatarFileStorage:
    def __init__(self, file, user):
        self._file = file
        self._user = user

    def update(self):
        new_avatar = {}
        image = Image.open(self._file)
        try:
            new_avatar = UserAvatar.objects.get(user=self._user)
        except UserAvatar.DoesNotExist:
            new_avatar = UserAvatar()
        finally:
            new_avatar.user = self._user
            new_avatar.avatar = image.tobytes()
            new_avatar.name = self._file.name
            new_avatar.height = image.height
            new_avatar.width = image.width
            new_avatar.format = image.format
            new_avatar.image_mode = image.mode
            new_avatar.save()


class AvatarFileRetrieval:
    def __init__(self, user):
        self.user = user

    def __get__(self):
        try:
            self.avatar = UserAvatar.objects.get(user=self.user)
        except UserAvatar.DoesNotExist:
            raise
        return self.avatar

    def getb64encodedimage(self):
        try:
            avatar = self.__get__()
            image = Image.frombytes(avatar.image_mode, (avatar.width, avatar.height), avatar.avatar.tobytes())
        except UserAvatar.DoesNotExist:
            raise
        except NameError:
            raise
        except AttributeError:
            raise
        else:
            buffered = BytesIO()
            image.save(buffered, format=avatar.format)
            buffered.seek(0)
            img_str = b64encode(buffered.read())
        return img_str

    def getavatarinstance(self):
        return self.__get__()
