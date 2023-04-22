from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.template.loader import render_to_string
# Create your views here.

pages_list = {
    "home": "Home!",
    "stories": "Stories",
    "mystories": "My Stories",
    "likedstories": "Liked Stories",
    "search": "Search",
    "addstories": "Add Stories",
}


def index(request):
    list_items = ""
    pages = list(pages_list.keys())

    for page in pages:
        page_path = reverse("pages", args=[page])
        list_items += f"<li><a href=\"{page_path}\">{page}</a></li>"

    response_data = f"<ul>{list_items}</ul>"
    return HttpResponse(response_data)


def pages(request, page):
    try:
        page_text = pages_list[page]
        response_data = render_to_string("storyTellerApp/home.html")
        return HttpResponse(response_data)
    except:
        HttpResponseNotFound("Page not found!")


def home_page(request):
    return render(request, "storyTellerApp/home.html")


def stories(request):
    pass


def view_story(request):
    pass


def editstories(request):
    return HttpResponse("Edit Stories")


def location(request):
    return HttpResponse("Location")