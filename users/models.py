from django.core.files.storage import FileSystemStorage
from django.db import models
from django.contrib.auth.models import AbstractUser

fs = FileSystemStorage(location="./users/media/")


class User(AbstractUser):
    avatar = models.ImageField(storage=fs, null=True)