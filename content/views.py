
import imp
from pprint import pformat
from typing import List
from urllib import response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from numpy import rec
from .forms import SignUpForm,LoginForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Song,Listen_Later,History,Favourite
from .recommend import recommend_songs
from .recommend import data
import json
from django.db.models import Case, When

from functools import reduce
from django.db.models import Q


# Create your views here.
def index(request):
    song=Song.objects.filter(tags="international").values()[0:5]
    his=History.objects.filter().order_by('-music_id')[:5:-1]

    ids=[]
    for i in his:
        ids.append(i.music_id)
    results=list(map(int, ids))

    queries = [Q(pk=value) for value in results]
    # Take one Q object from the list
    query = queries.pop()
    # Or the Q object with the ones remaining in the list
    for item in queries:
        query |= item
    song2=Song.objects.filter(query)
    return render(request,'content/index.html',{'songs':song,'history':song2})

def sign_up(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        if request.method=='POST':
            fm=SignUpForm(request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request,'You Have Created Your Account Now You can Login',extra_tags='signup')
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
                        messages.success(request,'You Have Successfully Logged',extra_tags='login')
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
        image="nepali.jfif"
    elif(playlist_u=="international"):
        image="international.webp"
    elif(playlist_u=="party"):
        image=" hp.webp"

       
    playlist=Song.objects.filter(tags=playlist_u)
    return render(request,'content/song_d.html',{'playlist':playlist,"image":image})



def song_c_o(request,id):
    song_c=Song.objects.filter(song_id=id).first()
    song_c2=Song.objects.filter(song_id=id).values()
    history=History.objects.filter()
    for i in history:
        if id==int(i.music_id):
            break
    else:
        his=History(music_id=id)
        his.save()

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
    else:
        return JsonResponse({'status': "Please Login To add Songs To Listen later"})             


def favourite(request):
    if request.user.is_authenticated:
        if request.method=='GET':
            status=0
            userL=request.user
            id=request.GET['history_id']

            favourite_coll=Favourite.objects.filter(user=userL)
            for i in favourite_coll:
                if id==i.music_id:  
                    break
            else:
                favColl=Favourite(user=userL,music_id=id)
                favColl.save()
                status=1
        return JsonResponse({'status':status})
    else:
        return JsonResponse({'status': "Please Login To add Songs To Favourite"})             

    


def show_ListenL(request):
    listen_p=Listen_Later.objects.filter(user=request.user)
    ids=[]
    for i in listen_p:
        ids.append(i.video_id)
    results = list(map(int, ids))

    # Turn list of values into list of Q objects
    queries = [Q(pk=value) for value in results]

    # Take one Q object from the list
    query = queries.pop()

# Or the Q object with the ones remaining in the list
    for item in queries:
        query |= item
    song=Song.objects.filter(query)
    return render(request,'content/listen_later.html',{'songs':song})


def search(request):
    query=request.GET['search']
    search =Song.objects.filter(name__icontains=query)
    return render(request,'content/search.html',{'searched_item':search})

def play_search(request,id):
    song=Song.objects.filter(song_id=id).first()
    return render(request,'content/playsearch.html',{'song':song})

def history(request):
    his=History.objects.filter()
    ids=[]
    for i in his:
        ids.append(i.music_id)
    results=list(map(int, ids))
    queries = [Q(pk=value) for value in results]

    # Take one Q object from the list
    query = queries.pop()

# Or the Q object with the ones remaining in the list
    for item in queries:
        query |= item
    song=Song.objects.filter(query)
    return render(request,'content/history.html',{'his':song})