from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default='')
    followers_number = models.PositiveIntegerField(default=0)
    following_number = models.PositiveIntegerField(default=0)
    followers = models.JSONField(default=list) 
    following = models.JSONField(default=list)
    picture = models.ImageField(upload_to = 'images/', default=False)

    def __str__(self):
        return f"{self.user} info"
