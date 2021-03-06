"""Nepfy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import imp
from django.contrib import admin
from django.urls import path
from Nepfy.settings import MEDIA_ROOT
from content import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='home'),
    path('signup/',views.sign_up,name='signup'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('playsong/<int:id>/',views.play_Song,name='play'),
    path('playlist/<playlist_u>/',views.playlist,name='playlist'),
    path('song_c_o/<int:id>/',views.song_c_o,name='song_c_o'),
    path('playnext',views.play_next,name='next'),
    path('previous',views.play_previous,name='previous'),
    path('Listen_L',views.listen_later,name='LL'),
    path('show_listen_later',views.show_ListenL,name='show_later'),
    path('search',views.search,name='search'),
    path('playsearch/<id>',views.play_search,name='playsearch'),
    path('history/',views.history,name='history'),
    path('favourite',views.favourite,name='favourite'),


] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
