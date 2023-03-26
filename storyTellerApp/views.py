from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse
# Create your views here.

pages_list = {
 "home" : "Home!",
 "mystories" : "My Stories",
 "likedstories" : "Liked Stories",
 "search" : "Search",
 "addstories" : "Add Stories",
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
      return HttpResponse(page_text)
    except: 
        HttpResponseNotFound("Page not found!")
    


def editstories(request):
    return HttpResponse("Edit Stories")

def location(request):
    return HttpResponse("Location")