from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('self', symmetrical=False, blank=True, related_name="followers")

class Tweet(models.Model):
    content = models.TextField()
    users_liked = models.ManyToManyField(User, blank=True, related_name="liked_tweets") 
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


