from django.contrib import admin
from django.urls import path
from .views import *
from .models import CustomUser

app_name = 'user'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/<str:username>', profile_view, name='profile'),
    path('edit/', edit_profile, name='edit')
]
