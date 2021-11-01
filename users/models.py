from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    """"A class to contain info abut the user"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default='')
    followers_number = models.PositiveIntegerField(default=0)
    following_number = models.PositiveIntegerField(default=0)
    followers = models.JSONField(default=list) 
    following = models.JSONField(default=list)
    bio_text = models.CharField(max_length=150, default='', blank=True)
    picture = models.ImageField(upload_to = 'images/', default=False, blank=True)

    def __str__(self):
        return f"{self.user} info"
