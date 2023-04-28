from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index),
    # path("<str:page>", views.pages, name="pages"),
    path("", views.home_page, name="home_page"),
    path("stories", views.stories, name="stories_page"),
    path("stories/<slug:slug>", views.view_story, name="view_story"),
]
