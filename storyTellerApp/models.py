from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
import uuid
from datetime import datetime

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
    profile_picture = models.ImageField(
        upload_to='profile_picture', default="profile_picture/blank_profile_picture_PDkAhtk.jpg")
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
    area = models.MultiPolygonField(blank=True, null=True)

    def __str__(self):
        return self.name 
    
class Story(models.Model):

    DATE_FORMAT_CHOICES = (
        (1, 'Exact Date'),
        (2, 'Range of Dates'),
        (3, 'Decade'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    date_format= models.IntegerField(choices=DATE_FORMAT_CHOICES)
    date_exact = models.DateField(null=True, blank=True)
    date_range_start= models.DateField(null=True, blank=True)
    date_range_end= models.DateField(null=True, blank=True)
    decade= models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    image= models.ImageField(upload_to='story_images', blank=True)

    def __str__(self):
        return self.user

    def __str__(self):
        return self.title

    def get_comments(self):
        return self.comment_set.all()

    def get_likes(self):
        return self.like_set.all()

    def get_tags(self):
        return self.tags.all()

    def get_location(self):
        return self.location


class Like(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)

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

    
