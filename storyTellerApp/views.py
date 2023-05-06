from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.template.loader import render_to_string
from datetime import date
from .models import Story
from .models import Profile
from .models import Location
from .models import Tag
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from geopy.geocoders import Nominatim
from django.contrib.gis.geos import Point, Polygon, LineString
import json
from .forms import StoryForm
from django.utils.html import strip_tags
import bleach
# Create your views here.

@login_required(login_url='login')
def home_page(request):
    latest_stories = Story.objects.all().order_by("-created_at")[:10]
    for story in latest_stories:
        cleaned_text = bleach.clean(story.content, tags=[], strip=True)
        text_without_images = bleach.clean(cleaned_text, tags=['p', 'a', 'strong', 'em', 'ul', 'ol', 'li', 'br'], strip=True)
        story.raw_text = strip_tags(text_without_images)
        if len(story.raw_text) > 100:
            story.raw_text = story.raw_text[:100] + '...'
        
    return render(request, "storyTellerApp/home.html",{ "stories" : latest_stories} )


def stories(request):
    return render( request, "storyTellerApp/stories.html", {
        "all_stories" : Story.objects.all().order_by("-created_at")
    })

def mystories(request):
    user_object= User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    return render( request, "storyTellerApp/mystories.html", {
        "my_stories" : Story.objects.filter(user=user_profile.id_user).order_by("-created_at")
    })

def view_story(request, id):
    identified_story = Story.objects.get(id=id)
    return render(request, "storyTellerApp/story.html", {"story": identified_story, "story_tags" : identified_story.tags.all(), "story_locations": identified_story.locations.all()})


def addstory(request):
    form = StoryForm()
    DATE_FORMAT_CHOICES = (
        (1, 'Exact Date'),
        (2, 'Session'),
        (3, 'Decade'),
        (4, 'Year'),
        (5, 'Month'),
        (6, 'Date Range'),
    )
    SESSION_CHOICES = (
        (1, 'fall'),
        (2, 'winter'),
        (3, 'spring'),
        (4, 'summer'),
    )
    DECADE_CHOICES = (
        (1, "2020's"),
        (2, "2010's"),
        (3, "2000's"),
        (4, "1990's"),
        (5, "1980's"),
        (6, "1970's"),
        (7, "1960's"),
        (8, "1950's"),
    )
    MONTH_CHOICES = (
        (1, "January"),
        (2, "February"),
        (3, "March"),
        (4, "April"),
        (5, "May"),
        (6, "June"),
        (7, "August"),
        (8, "September"),
        (9, "October"),
        (10, "November"),
        (11, "December"),
    )

    if request.method == 'POST':
        print(request.POST)
        form = StoryForm(request.POST)
        user = request.user
        title = request.POST["title"]
        content = request.POST["content"]
        #tag 
        tag = request.POST["tags"]
        tag_list = [t.strip() for t in tag.split(",")]
        tagList = []
        for tags in tag_list:
            tags = Tag(name= tags)
            tagList.append(tags)
            
        # location
        search_location = request.POST["coordinatessearch"]
        search_address = request.POST["address"]
        geolocator = Nominatim(user_agent="my_app")  
        loc_data_str = request.POST.get("locations", '[]')
        # date
        date_format = request.POST["date-format"]
        if 'exact_date' in request.POST:
            exact_date = request.POST['exact_date']
        else:
            exact_date = None
        if 'session' in request.POST:
            session = request.POST['session']
           
        else:
            session = None
        if 'decade' in request.POST:
            decade = request.POST['decade']
           
        else:
            decade = None
        if 'year' in request.POST:
            year = request.POST['year']
        else:
            year = None
        if 'month' in request.POST:
            month = request.POST['month']
           
        else:
            month = None
        if 'date-range-start' in request.POST:
            date_range_start = request.POST['date-range-start']
        else:
            date_range_start = None
        if 'date-range-end' in request.POST:
            date_range_end = request.POST['date-range-end']
        else:
            date_range_end = None

        if loc_data_str:
            loc_data = json.loads(loc_data_str)
        else:
            loc_data = []

        print(loc_data)
        locations = []
        if loc_data != []:
            for loc in loc_data:
                if loc.get('geometry'):
                    location_type = loc['geometry']['type']
                    coordinates = loc['geometry']['coordinates']

                    if location_type == 'Point':
                        point = Point(coordinates)
                        results = geolocator.reverse(f"{point.y}, {point.x}")
                        location_name = results.address
                        location_name = location_name.replace("unnamed road,", "")
                        print(location_name)
                        location = Location(name=location_name, point=point)

                    elif location_type == 'Polygon':
                        polygon = Polygon(coordinates[0])
                        centroid = polygon.centroid
                        results = geolocator.reverse(f"{centroid.y}, {centroid.x}" )
                        location_name = results.address
                        location_name = location_name.replace("unnamed road,", "")
                        print(location_name)
                        location = Location(
                            name=location_name, area=polygon)

                    elif location_type == 'LineString':
                        linestring = LineString(coordinates)
                        midpoint = linestring.interpolate(linestring.length/2)
                        results = geolocator.reverse(f"{midpoint.y}, {midpoint.x}")
                        location_name = results.address
                        location_name = location_name.replace("unnamed road,", "")
                        print(location_name)
                        location = Location(
                            name=location_name, lines=linestring)

                    if location:
                        radius = loc.get('properties', {}).get('radius')
                        if radius:
                            location.radius = float(radius)

                    locations.append(location)
        else:
            x, y= search_location.split(", ")
            search_point = Point(float(x), float(y))
            search_name = search_address
            location_search = Location(name=search_name, point=search_point)
            locations.append(location_search)
            
        print(locations)

        for location in locations:
            location.save()
        
        for tags in tagList:
            tags.save()

      
        new_story= Story.objects.create(
            user=user,
            content= content, 
            date_format=date_format,
            session = session,
            month = month,
            year = year,
            date_exact= exact_date,
            date_range_start = date_range_start,
            date_range_end = date_range_end,
            decade = decade,
            title=title,
            )
        new_story.save()
        new_story.locations.set(locations)
        new_story.tags.set(tagList)
        
       
        return redirect('/')

    else:
        context = {'form': form, 'DATE_FORMAT_CHOICES': DATE_FORMAT_CHOICES, 'SESSION_CHOICES': SESSION_CHOICES, 'DECADE_CHOICES':DECADE_CHOICES, 'MONTH_CHOICES': MONTH_CHOICES}
        return render(request, 'storyTellerApp/addstory.html', context)




def editstories(request):
    return HttpResponse("Edit Stories")


def signup(request):

    if request.method == "POST":
        username= request.POST['username']
        email= request.POST['email']
        password= request.POST['password']
        password2= request.POST['password2']
        firstname= request.POST['firstname']
        lastname= request.POST['lastname']

        if password== password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email taken")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,"Username taken")
                return redirect('signup')
            else: 
                user = User.objects.create_user(username=username, email=email,password=password, first_name=firstname, last_name=lastname)
                user.save()

                user_model=User.objects.get(username=username)
                new_profile= Profile.objects.create(user=user_model, id_user=user_model.id, username=user_model.username, first_name=user_model.first_name, last_name=user_model.last_name, email=user_model.email, password=user_model.password )
                new_profile.save()
                return redirect('login')
        else:
            messages.info(request, "Password not maching")
            return redirect('signup')

    else:
        return render(request, 'storyTellerApp/signup.html')


def login(request):
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']

        user= auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('home_page')
        else:
            messages.info(request, 'Invalid creditials')
            return redirect('login')
    else:
        return render(request, 'storyTellerApp/login.html')

@login_required(login_url='login')    
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')    
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method =='POST':
        if request.FILES.get('profile_image') == None:
            image= user_profile.profile_picture
            bio= request.POST['bio']

            user_profile.profile_picture = image
            user_profile.bio = bio
            user_profile.save()
        if request.FILES.get('profile_image') !=None:
            image= request.FILES.get('profile_image')
            bio= request.POST.get('bio')

            user_profile.profile_picture = image
            user_profile.bio = bio
            user_profile.save()
        
        return redirect('settings')
    
    return render(request, "storyTellerApp/profile_settings.html", {'user_profile': user_profile})
