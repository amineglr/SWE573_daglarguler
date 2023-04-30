from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.template.loader import render_to_string
from datetime import date
from .models import Story
from .models import Profile
from .models import Location
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def home_page(request):
    latest_stories = Story.objects.all().order_by("-created_at")[:10]
    return render(request, "storyTellerApp/home.html",{ "stories" : latest_stories} )


def stories(request):
    return render( request, "storyTellerApp/stories.html", {
        "all_stories" : Story.objects.all().order_by("-created_at")
    })

def mystories(request):
    user_object= User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    return render( request, "storyTellerApp/mystories.html", {
        "my_stories" : Story.objects.filter(user=user_profile.id_user)
    })

def view_story(request, id):
    identified_story = Story.objects.get(id=id)
    return render(request, "storyTellerApp/story.html", {"story": identified_story, "story_tags" : identified_story.tags.all()})


def addstory(request):
    if request.method== "POST":
        user = request.user
        image= request.FILES.get("media")
        title = request.POST["content"]
        content = request.POST["title"]
        if request.POST["session"] !=None:
            new_story= Story.objects.create(user=user, image=image, content=content, date_format='2', title=title, location=Location(id='aaa16712-f6e0-4af6-88b8-228a763a90ad', name='east-turkey'))
        elif request.POST["decade"] !=None :
            new_story= Story.objects.create(user=user, image=image, content=content, date_format='3', title=title, location=Location(id='aaa16712-f6e0-4af6-88b8-228a763a90ad', name='east-turkey'))
        elif request.POST["year"] !=None :
            new_story= Story.objects.create(user=user, image=image, content=content, date_format='4', title=title, location=Location(id='aaa16712-f6e0-4af6-88b8-228a763a90ad', name='east-turkey'))
        elif request.POST["month"] !=None :
            new_story= Story.objects.create(user=user, image=image, content=content, date_format='5', title=title, location=Location(id='aaa16712-f6e0-4af6-88b8-228a763a90ad', name='east-turkey'))
        else:
            new_story= Story.objects.create(user=user, image=image, content=content, date_format='1',title=title, location=Location(id='aaa16712-f6e0-4af6-88b8-228a763a90ad', name='east-turkey'))
        
        new_story.save()
        return redirect('/')

    else:
        return render(request, 'storyTellerApp/addstory.html')




def editstories(request):
    return HttpResponse("Edit Stories")


def location(request):
    return HttpResponse("Location")

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
