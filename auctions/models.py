from django.contrib.auth.models import AbstractUser
from django.db import models


    

class Categories(models.Model):
    category = models.TextField(max_length=128)
    def __str__(self):
        return f"{self.category}" 

class Listings(models.Model):
    title = models.TextField(max_length=64)
    description = models.TextField(max_length=128)
    picture = models.ImageField(upload_to="commerce/media/listing_pics")
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='listings')
    time = models.DateTimeField(auto_now=True) 
    lister = models.TextField(max_length=32)
    active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.title} on {self.time} by {self.lister}"

class Comments(models.Model):
    text = models.TextField(max_length=128)
    user = models.TextField(max_length=32)
    product = models.ForeignKey(Listings, on_delete=models.CASCADE,related_name="comments")
    def __str__(self):
        return f"{self.text}"

class Bids(models.Model):
    user = models.TextField(max_length=32) 
    bid = models.IntegerField()
    product = models.ForeignKey(Listings,on_delete=models.CASCADE,related_name="bids")
    def __str__(self):
        return f"{self.bid}"




class User(AbstractUser):
    watchlist = models.ManyToManyField(Listings, related_name="users",blank=True)


    


