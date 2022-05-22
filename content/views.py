
import imp
from pprint import pformat
from typing import List
from urllib import response
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from numpy import rec
from .forms import SignUpForm,LoginForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Song
from .recommend import recommend_songs
from .recommend import data
import json
from joblib import load

# Create your views here.

model=load('./notebooks/models.joblib')
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
    recommendSongs =recommend_songs([{'name': 'Come As You Are', 'year':1991}],data)
    return render(request,'content/playsong.html',{'song':song,'recommend_songs':recommendSongs})


def playlist(request):
    playlist=Song.objects.filter(tags="Love Hits")
    return render(request,'content/song_d.html',{'playlist':playlist})



def song_c_o(request,id):
    playlist=Song.objects.filter(tags="Love Hits")
    song_c=Song.objects.filter(song_id=id).first
    return render(request,'content/songd_p.html',{'playlist':playlist,'songC':song_c})

def play_next(request):
    id=request.GET['s_id']
    playlist=Song.objects.filter(tags="Love Hits").values()
    filter_playlist=list(playlist)    
    return JsonResponse({'status':'save','filter_playlist':filter_playlist, 'song_id':id})


def play_previous(request):
    playlist=Song.objects.filter(tags="Love Hits").values()
    filter_playlist=list(playlist) 
    return JsonResponse({'status':'previous','filter_playlist':filter_playlist})