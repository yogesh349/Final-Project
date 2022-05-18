
import imp
from pprint import pformat
from typing import List
from urllib import response
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .forms import SignUpForm,LoginForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Song
import json

# Create your views here.

def index(request):
    song=Song.objects.all()[:5]

    return render(request,'content/index.html',{'songs':song})

def sign_up(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        if request.method=='POST':
            fm=SignUpForm(request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request,'You Have Successfully Logged')
                return HttpResponseRedirect('/')
        else:
            fm=SignUpForm()

    return render(request,'content/signup.html',{'form':fm})


def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
            if request.method=='POST':
                fm=LoginForm(request=request,data=request.POST)
                if fm.is_valid():
                    user=authenticate(username=fm.cleaned_data['username'],password=fm.cleaned_data['password'])
                    if user is not None:
                        print("Not yet login")
                        login(request,user)
                        messages.success(request,'You Have Successfully Logged')
                        return HttpResponseRedirect('/')
            else:
                fm=LoginForm()
            return render(request,'content/login.html',{'form':fm})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def play_Song(request,id):
    song=Song.objects.filter(song_id=id).first()
    return render(request,'content/playsong.html',{'song':song})


def playlist(request):
    playlist=Song.objects.filter(tags="Love Hits")
    return render(request,'content/song_d.html',{'playlist':playlist})

# def song_s(request):
#     if request.method=="GET":
#         id=request.GET['song_id']
#         song_c=Song.objects.filter(song_id=id).first()
#         song_choose=json.dumps(song_c)
#         return JsonResponse({'status':'save','song_choose': song_choose})


def song_c_o(request,id):
    playlist=Song.objects.filter(tags="Love Hits")
    song_c=Song.objects.filter(song_id=id).first
    return render(request,'content/songd_p.html',{'playlist':playlist,'songC':song_c})