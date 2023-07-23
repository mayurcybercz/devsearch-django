from django.shortcuts import render
from django.http import HttpResponse

def profiles(request):
    context={}
    return render(request,'users/profiles.html',context)