from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import SignUpForm

# Create your views here.

def index(request):
    return render(request,'content/index.html')

def sign_up(request):
    if request.method=='POST':
        fm=SignUpForm(request.POST)
        if fm.is_valid():
            fm.save()
            return HttpResponseRedirect('/')
    else:
        fm=SignUpForm()
    
    return render(request,'content/signup.html',{'form':fm})
