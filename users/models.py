from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    followers_number = models.PositiveIntegerField(default=0)
    following_number = models.PositiveIntegerField(default=0)
    followers = models.JSONField(default=list) 
    following = models.JSONField(default=list)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
