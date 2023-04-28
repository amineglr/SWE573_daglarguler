from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.template.loader import render_to_string
from datetime import date
# Create your views here.

pages_list = {
    "home": "Home!",
    "stories": "Stories",
    "mystories": "My Stories",
    "likedstories": "Liked Stories",
    "search": "Search",
    "addstories": "Add Stories",
}

all_stories = [
    {
        "slug" : "1",
        "author" : "amineglr",
        "date" : date(2023, 4,28),
        "title" :"Travel With Train",
        "excerpt" : "Summary",
        "content" : " example story", 

    },
    {
        "slug" : "2",
        "author" : "amineglr",
        "date" : date(2022, 4,28),
        "title" :"Travel With Bus",
        "excerpt" : "Summary",
        "content" : " example story", 

    },
    {
        "slug" : "3",
        "author" : "amineglr",
        "date" : date(2022, 4,28),
        "title" :"Travel With Bus",
        "excerpt" : "Summary",
        "content" : " example story", 

    }
]


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

def get_date(story):
    return story['date']

def home_page(request):
    sorted_stories = sorted(all_stories, key=get_date)
    latest_stories= sorted_stories[-10:]
    return render(request, "storyTellerApp/home.html",{ "stories" : latest_stories} )


def stories(request):
    return render( request, "storyTellerApp/stories.html")


def view_story(request, slug):
    return render(request, "storyTellerApp/story.html")


def editstories(request):
    return HttpResponse("Edit Stories")


def location(request):
    return HttpResponse("Location")
