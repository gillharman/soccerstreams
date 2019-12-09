from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class UserAvatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.BinaryField()
    avatar_name = models.CharField(max_length=140)
    avatar_width = models.IntegerField()
    avatar_height = models.IntegerField()
    avatar_size = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)