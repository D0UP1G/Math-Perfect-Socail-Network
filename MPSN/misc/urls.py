from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'misc'

urlpatterns = [
    path('leaderboard/', leaderboard_view, name='leaderboard'),
    path('', home_view, name='home'),
]
