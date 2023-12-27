from django.urls import path
from .views import UserProfileList
from . import views

urlpatterns = [
    path('user_profile/', UserProfileList.as_view(), name='user_profile'),

]

