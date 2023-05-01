from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("stories", views.stories, name="stories_page"),
    path("stories/<slug:id>", views.view_story, name="view_story"),
    path("signup", views.signup, name="signup"),
    path("login", views.login, name="login"),
    path("signout", views.logout, name="signout"),
    path("settings", views.settings, name="settings"),
    path("addstory", views.addstory, name="addstory"),
    path("mystories", views.mystories, name="mystories"),
]
