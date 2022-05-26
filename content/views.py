
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
from .models import Song,Listen_Later
from .recommend import recommend_songs
from .recommend import data
import json

from functools import reduce
from django.db.models import Q

# Create your views here.
def index(request):
    song=Song.objects.filter(tags="international").values()[0:5]
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
    song_rec=Song.objects.filter(song_id=id).values()
    filter_song_rec=list(song_rec)
    name=filter_song_rec[0]['name']
    year=int(filter_song_rec[0]['year'])
    recommendSongs =recommend_songs([{'name': name, 'year':year}],data)
    return render(request,'content/playsong.html',{'song':song,'recommend_songs':recommendSongs})



def playlist(request,playlist_u):
    if(playlist_u)=="Love Hits":
        image="LH.jpg"
    elif(playlist_u=="nepali"):
        image="nepali.jpeg"
    elif(playlist_u=="international"):
        image="international.webp"
    playlist=Song.objects.filter(tags=playlist_u)
    return render(request,'content/song_d.html',{'playlist':playlist,"image":image})



def song_c_o(request,id):
    song_c=Song.objects.filter(song_id=id).first()
    song_c2=Song.objects.filter(song_id=id).values()
    song_list_filter=list(song_c2)
    song_tags=song_list_filter[0]['tags']
    playlist=Song.objects.filter(tags=song_tags).values()
    if song_tags=="Love Hits":
        image="LH.jpg"
    elif(song_tags=="nepali"):
        image="nepali.jpeg"
    elif(song_tags=="international"):
        image="international.webp"
    return render(request,'content/songd_p.html',{'playlist':playlist,'songC':song_c})

def play_next(request):
    id=request.GET['s_id']
    song_next=Song.objects.filter(song_id=id).values()
    song_list_filter=list(song_next)
    song_tags=song_list_filter[0]['tags']
    playlist=Song.objects.filter(tags= song_tags).values()
    filter_playlist=list(playlist)    
    return JsonResponse({'status':'save','filter_playlist':filter_playlist, 'song_id':id})


def play_previous(request):
    id=request.GET['s_id']
    song_next=Song.objects.filter(song_id=id).values()
    song_list_filter=list(song_next)
    song_tags=song_list_filter[0]['tags']
    playlist=Song.objects.filter(tags=song_tags).values()
    filter_playlist=list(playlist) 
    return JsonResponse({'status':'previous','filter_playlist':filter_playlist})


def listen_later(request):
    if request.user.is_authenticated:
        if request.method=='GET':
            status=0
            userL=request.user
            l_id=request.GET['listen_l']
            later=Listen_Later.objects.filter(user=userL)
            for i in later:
                if l_id==i.video_id:
                    break
            else:
                listenLater=Listen_Later(user=userL,video_id=l_id)
                listenLater.save()
                status=1
    return JsonResponse({'status':status})



def show_ListenL(request):
    listen_p=Listen_Later.objects.filter(user=request.user)
    ids=[]
    for i in listen_p:
        ids.append(i.video_id)
    
    results = list(map(int, ids))
    song=Song.objects.filter(song_id_in=query)

    return render(request,'content/listen_later.html',{'songs':song})