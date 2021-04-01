from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    Location = models.CharField(max_length=100)

    def __str__(self):
        return self.Location


class Dates(models.Model):
    date_posted = models.DateField()
    img1 = models.ImageField(upload_to='pics')
    count1 = models.IntegerField()
    img2 = models.ImageField(upload_to='pics')
    count2 = models.IntegerField()
    location = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __int__(self):
        return self.location
