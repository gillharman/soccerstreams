from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


# class UserAvatar(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     avatar_bytes = models.BinaryField()
#     name = models.CharField(max_length=140)
#     width = models.IntegerField()
#     height = models.IntegerField()
#     format = models.CharField(max_length=10, null=True)
#     image_mode = models.CharField(max_length=10)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)