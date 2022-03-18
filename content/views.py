
from urllib import response
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import SignUpForm,LoginForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request,'content/index.html')

def sign_up(request):
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