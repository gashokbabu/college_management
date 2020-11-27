from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	class Meta:
		model = User  #here if u save the form it get into User model or in simple the form save to user
		fields = ['username','email','password1','password2']
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email']

class SetProfileForm(forms.ModelForm):
	class Meta:
		model = CurrentStudent
		fields = ['AcadamicYear','name','regNo','Year','Sem','section','joinedYear','teacher']

class ProfilePicForm(forms.ModelForm):
    class Meta:
    	model = CurrentStudent
    	fields =['profile_pic']