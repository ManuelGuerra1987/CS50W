from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True, related_name="watchlist")  


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_price = models.DecimalField(decimal_places=2, max_digits=8)
    current_price = models.DecimalField(decimal_places=2, max_digits=8)
    url_image = models.URLField(max_length=300)
    category = models.CharField(max_length=64)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_open = models.BooleanField(default=True)
    current_winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="winning_listings")

  

class Comment(models.Model):
    text = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

class Bid(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=8)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
 
