from django.contrib.gis import admin
from .models import Profile, Tag, Story , Comment ,Like , Location , Follower

admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Story)
admin.site.register(Like)
admin.site.register(Location)
admin.site.register(Follower)