from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("<str:page>", views.pages, name="pages")
]