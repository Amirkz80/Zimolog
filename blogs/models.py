from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    """Contains a title and texts about each title"""
    title = models.CharField(max_length=200)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)

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