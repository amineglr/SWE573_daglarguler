from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
import uuid
from datetime import datetime
from ckeditor.fields import RichTextField


# Create your models here.

User = get_user_model()

class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    point = models.PointField(blank=True, null=True)
    area = models.PolygonField(blank=True, null=True)
    lines= models.LineStringField(blank=True, null=True)
    radius = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name 
    
class Story(models.Model):

    DATE_FORMAT_CHOICES = (
        (1, 'choose a date type'),
        (2, 'Exact Date'),
        (3, 'Session'),
        (4, 'Decade'),
        (5, 'Year'),
        (6, 'Month'),
        (7, 'Date Range'),
    )
    SESSION_CHOICES = (
        (1, 'choose a session'),
        (2, 'fall'),
        (3, 'winter'),
        (4, 'spring'),
        (5, 'summer'),
    )
    DECADE_CHOICES = (
        (1, "choose a decade"),
        (2, "2020's"),
        (3, "2010's"),
        (4, "2000's"),
        (5, "1990's"),
        (6, "1980's"),
        (7, "1970's"),
        (8, "1960's"),
        (9, "1950's"),
    )
    MONTH_CHOICES = (
        (1, "choose a month"),
        (2, "January"),
        (3, "February"),
        (4, "March"),
        (5, "April"),
        (6, "May"),
        (7, "June"),
        (8, "August"),
        (9, "September"),
        (10, "October"),
        (11, "November"),
        (12, "December"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    date_format= models.IntegerField(choices=DATE_FORMAT_CHOICES,null=True, blank=True)
    session = models.CharField(choices=SESSION_CHOICES,null=True, blank=True, max_length=100)
    month = models.CharField(choices=MONTH_CHOICES,null=True, blank=True, max_length=100)
    year = models.CharField(max_length=100, null=True, blank=True)
    date_exact = models.DateField(null=True, blank=True)
    date_range_start= models.CharField(max_length=100, null=True, blank=True)
    date_range_end= models.CharField(max_length=100, null=True, blank=True)
    decade= models.CharField(choices=DECADE_CHOICES,null=True, blank=True, max_length=100)
    tags = models.ManyToManyField(Tag, blank=True)
    locations =  models.ManyToManyField(Location)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_comments(self):
        return self.comment_set.all()

    def get_likes(self):
        return self.like_set.all()

    def get_tags(self):
        return self.tags.all()

    def get_location(self):
        return self.locations.all()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100,  default="")
    username = models.CharField(max_length=50, unique=True, default="")
    email = models.EmailField(unique=True, default="")
    password = models.CharField(max_length=128, default="")
    profile_picture = models.FileField(
        upload_to='profile_picture/', default="profile_picture/blank_profile_picture_PDkAhtk.jpg")
    bio = models.TextField(blank=True)
    likedstories = models.ManyToManyField(Story)

    def __str__(self):
        return self.user.username

class Like(models.Model):
    story_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)
    def __str__(self):
        return self.username

class Comment(models.Model):
    username = models.CharField(max_length=100)
    content=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="comments")


    def __str__(self):
        return self.username

class Follower(models.Model):
    user = models.CharField(max_length=100)
    follower = models.CharField(max_length=100)
    def __str__(self):
        return self.user

    
