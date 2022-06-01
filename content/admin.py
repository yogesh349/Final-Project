from django.contrib import admin
from . models import Song, Listen_Later,History,Favourite
# Register your models here.
admin.site.register(Song)
admin.site.register(Listen_Later)
admin.site.register(History)
admin.site.register(Favourite)