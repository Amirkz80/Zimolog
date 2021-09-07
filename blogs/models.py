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