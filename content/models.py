from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Song(models.Model):
    song_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=2000)
    singer= models.CharField(max_length=2000)
    tags= models.CharField(max_length=100)
    image=models.ImageField(upload_to="images")
    song=models.FileField(upload_to="music")
    duration=models.CharField(max_length=100, default='2')
    year = models.CharField(max_length=300, default='')

    def __str__(self):
        return self.name


class Listen_Later(models.Model):
    watch_id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    video_id=models.CharField(max_length=100000,default="")

class History(models.Model):
    history_id=models.AutoField(primary_key=True)
    music_id=models.CharField(max_length=100000,default="")


class Favourite(models.Model):
    favourite_id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    music_id=models.CharField(max_length=100000,default="")
