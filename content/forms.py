from dataclasses import fields
from pyexpat import model
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django import forms


class SignUpForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model=User
        fields =['username','first_name','last_name','email']            


class LoginForm(AuthenticationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control custom-form'}))
    password=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))

