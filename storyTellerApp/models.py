from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
import uuid
from datetime import datetime
from ckeditor.fields import RichTextField


# Create your models here.

User = get_user_model()


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

    def __str__(self):
        return self.user.username

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
        (1, 'Exact Date'),
        (2, 'Session'),
        (3, 'Decade'),
        (4, 'Year'),
        (5, 'Month'),
        (6, 'Date Range'),
    )
    SESSION_CHOICES = (
        (1, 'fall'),
        (2, 'winter'),
        (3, 'spring'),
        (4, 'summer'),
    )
    DECADE_CHOICES = (
        (1, "2020's"),
        (2, "2010's"),
        (3, "2000's"),
        (4, "1990's"),
        (5, "1980's"),
        (6, "1970's"),
        (7, "1960's"),
        (8, "1950's"),
    )
    MONTH_CHOICES = (
        (1, "January"),
        (2, "February"),
        (3, "March"),
        (4, "April"),
        (5, "May"),
        (6, "June"),
        (7, "August"),
        (8, "September"),
        (9, "October"),
        (10, "November"),
        (11, "December"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    date_format= models.IntegerField(choices=DATE_FORMAT_CHOICES)
    session = models.CharField(choices=SESSION_CHOICES, null=True, blank=True,max_length=20)
    month = models.CharField(choices=MONTH_CHOICES, null=True, blank=True,max_length=20 )
    year = models.CharField(max_length=100, null=True, blank=True)
    date_exact = models.DateField(null=True, blank=True)
    date_range_start= models.CharField(max_length=100, null=True, blank=True)
    date_range_end= models.CharField(max_length=100, null=True, blank=True)
    decade= models.CharField(choices=DECADE_CHOICES, null=True, blank=True, max_length=20)
    tags = models.ManyToManyField(Tag, blank=True)
    locations =  models.ManyToManyField(Location)
    no_of_likes = models.IntegerField(default=0)
    liked = models.IntegerField(default=0)

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


class Like(models.Model):
    story_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)
    def __str__(self):
        return self.username

class Comment(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)
    content=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)


    def __str__(self):
        return self.username

class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    def __str__(self):
        return f"{self.follower.username} follows {self.user.username}"

    
