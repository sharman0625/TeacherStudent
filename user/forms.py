from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from chat.models import *

class CreateUserForm(UserCreationForm):
    PROFESSION_CHOICES = (
            ('student', 'student'),
            ('teacher', 'teacher'),
        )
    profession = forms.ChoiceField(choices = PROFESSION_CHOICES) 
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'profession']