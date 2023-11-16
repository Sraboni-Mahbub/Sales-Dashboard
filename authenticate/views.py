from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.urls import reverse, reverse_lazy
import os
import logging
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from authenticate.models import UserProfile
from authenticate.forms import CreateNewUser, ProfilePictureForm


# Create your views here.

def loginPage(request):
    if request.user.is_superuser:
        messages.error(request, 'You are a superuser')
        return HttpResponseRedirect('login')
    else:
        if request.user.is_authenticated:
            return redirect('/')

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is None:
                messages.info(request, 'Username or password wrong')
                return redirect('login')
            else:
                login(request, user)
                return redirect('/')

    return render(request, 'authenticate/login.html')


@login_required(login_url='/authenticate/login/')
def Create_User(request):
    form = CreateNewUser()
    if request.method == 'POST':
        form = CreateNewUser(data=request.POST)
        if form.is_valid():
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['password1']

            pin = request.POST['pin']
            if UserProfile.objects.filter(pin=pin).exists():
                messages.info(request, 'PIN already exists')
                return redirect('create_user')

            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            data_dict = {
                'user_id': user.id,
                'full_name': request.POST['full_name'],
                'job_title': request.POST['job_title'],
                'pin': pin,
                'role_type': request.POST['role_type'],
            }
            UserProfile.objects.create(**data_dict, head_of_sales_id=request.user.id)
            return redirect('user')

    return render(request, "authenticate/create_user.html", {'form': form})


@login_required(login_url='/authenticate/login/')
def UserList(request):
    if request.user.user_profile.role_type == 'HOS':
        hos_user = request.user
        users = UserProfile.objects.filter(role_type='Salesperson', head_of_sales=hos_user)

    elif request.user.user_profile.role_type == 'CEO':
        users = UserProfile.objects.exclude(role_type='CEO')

    else:
        raise Http404('Access Denied')

    if request.method == 'GET':
        username = request.GET.get('username', '')
        query = Q()
        # Filter based on the 'user' field in UserProfile
        query &= Q(user__username=username)
        results = UserProfile.objects.filter(query)

    diction = {
        'title': 'User List',
        'users': users,
        'results': results
    }

    return render(request, "authenticate/user.html", context=diction)

@login_required(login_url='/authenticate/login/')
def update_user_info(request, user_id):
    user_profile = UserProfile.objects.get(pk=user_id)


    if request.method == 'POST':

        user_profile.full_name = request.POST.get('full_name')
        user_profile.job_title = request.POST.get('job_title')
        user_profile.role_type = request.POST.get('role_type')


        user_profile.save()
        user_email = user_profile.user.email

        return redirect('user')

    return render(request, "authenticate/update_user_info.html",{'user_profile': user_profile})

@login_required(login_url='/authenticate/login/')
def view_user(request, user_id):
    user_profile = UserProfile.objects.get(pk=user_id)
    return render(request, "authenticate/view_user.html", {'user_profile': user_profile})


@login_required(login_url='/authenticate/login/')
def profile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            # Check if there's an existing profile picture to remove
            if user_profile.profile_picture:
                # Remove the existing profile picture file
                default_storage.delete(user_profile.profile_picture.name)

            # Save the new profile picture
            profile_picture = form.cleaned_data.get('profile_picture')
            if profile_picture:
                user_profile.profile_picture = profile_picture
            else:
                user_profile.profile_picture = None  # Clear the profile picture

            user_profile.save()
            return redirect('profile')  # Replace 'profile' with the URL name for the user's profile page
    else:
        form = ProfilePictureForm(instance=user_profile)

    return render(request, "authenticate/profile.html", {'user': user, 'user_profile': user_profile, 'form': form})


@login_required(login_url='/authenticate/login/')
def edit_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        user_profile.full_name = request.POST.get('full_name')
        user_profile.job_title = request.POST.get('job_title')
        user_profile.role_type = request.POST.get('role_type')

        user_profile.save()

        return redirect('profile')

    return render(request, "authenticate/edit_profile.html", {'user_profile': user_profile})


@login_required(login_url='/authenticate/login/')
def logoutUser(request):
    logout(request)
    return redirect('login')
