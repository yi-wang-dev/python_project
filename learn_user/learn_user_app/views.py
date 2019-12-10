from django.shortcuts import render
from learn_user_app.forms import UserForm,UserProfileInfoForm
from django.contrib.auth.models import User
# Create your views here.

def index(request):
    return render(request,'learn_user_app/index.html')

def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        user_profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = user_profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors, user_profile_form.errors)
    else:
        user_form = UserForm()
        user_profile_form = UserProfileInfoForm()

    return render(request,"learn_user_app/register.html",{
        "user_form":user_form,
        "user_profile_form":user_profile_form,
        "registered":registered
    })

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request,username=username,password=password)

        if user and user.is_active:
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
        else:
            print("not active")
    else:
        return render(request,"learn_user_app/login.html")
@login_required
def user_logout(request):
    logout(request)
    return reverse("index")
