from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index),
    # path("<str:page>", views.pages, name="pages"),
    path("", views.home_page, name="home_page"),
    path("stories", views.stories, name="stories_page"),
    path("stories/<slug:id>", views.view_story, name="view_story"),
    path("signup", views.signup, name="signup"),
    path("login", views.login, name="login"),
]
