from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from authenticate.models import *

class CreateNewUser(UserCreationForm):
    email = forms.EmailField(required=True, label="", widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    username = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(
        required=True, label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        required=True, label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password Confirm'})
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('full_name', 'job_title', 'head_of_sales', 'role_type', 'sales_category')

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']