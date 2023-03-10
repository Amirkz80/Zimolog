from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    """Contains a title and texts about each title"""
    title = models.CharField(default='', max_length=100)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    heart = models.PositiveIntegerField(default=0)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    people_who_liked = models.JSONField(default=list)

    def __str__(self):
        """Retrurns a represntation of the model"""
        if len(self.text) >= 30:
            return (f"{self.title}, {self.text[:31]}...") 
        else:
            return (f"{self.title}, {self.text}")


class Comments(models.Model):
    """Contains text and the date of the user's comment"""
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        """Retrurns a represntation of the model"""
        if len(self.text) >= 30:
            return (f"{self.text[:31]}...") 
        else:
            return (f"{self.text}")