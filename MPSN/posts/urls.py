from django.contrib import admin
from django.urls import path
from .views import *
app_name = 'posts'

urlpatterns = [
    path('create/', create_post_view, name='create'),
]
