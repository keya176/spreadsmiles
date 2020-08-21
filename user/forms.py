from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EventForm(forms.ModelForm):
     class Meta:
         model = Event
         fields = '__all__'
class Createuser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

