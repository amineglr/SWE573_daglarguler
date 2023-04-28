from django.contrib.gis import admin
from .models import Profile, Tag, Story , Comment ,Like , Location , Follower


class StoryAdmin(admin.ModelAdmin):
    list_filter =("user", "tags")
    list_display =("title","user")

admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Story, StoryAdmin)
admin.site.register(Like)
admin.site.register(Location)
admin.site.register(Follower)