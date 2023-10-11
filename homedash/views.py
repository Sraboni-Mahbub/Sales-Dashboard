from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .models import *
#from .forms import *

@login_required(login_url='/authenticate/login/')
def home(request):
    return render(request, 'homedash/index.html')

