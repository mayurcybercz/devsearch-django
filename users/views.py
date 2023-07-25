from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile
from .forms import customUserCreationForm

def loginUser(request):
    page='login'
    context={'page':page}
    if request.user.is_authenticated:
        return render('profiles')
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'Username does not exist')

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('profiles')
        else:
            messages.error(request,'Username OR password is incorrect')
    return render(request,'users/login_register.html',context)

def logoutUser(request):
    logout(request)
    messages.success(request,'User successfully logged out!')
    return(redirect('login'))

def registerUser(request):
    page='register'
    form=customUserCreationForm()
    if request.method=="POST":
        form=customUserCreationForm(request.POST)
        print("inpost")
        if form.is_valid():
            user=form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            print("useradded")
            messages.success(request,"User account created!")

            login(request,user)
            return redirect('profiles')
        else:
            messages.error(request,"Error occurred during registration")
    context={'page':page,'form':form}
    return render(request,'users/login_register.html',context)

def profiles(request):
    profiles=Profile.objects.all()
    context={'profiles':profiles}
    return render(request,'users/profiles.html',context)

def userProfile(request,pk):
    profile=Profile.objects.get(id=pk)
    topSkills=profile.skill_set.exclude(description__exact="")
    otherSkills=profile.skill_set.filter(description="")
    context={'profile':profile,'topSkills':topSkills,'otherSkills':otherSkills}
    return render(request,'users/user-profile.html',context)