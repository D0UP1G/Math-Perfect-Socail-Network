from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'user'

urlpatterns = [
	path('profile/', profile, name='profile'),
	path('accounts/registration/', RegisterView.as_view(), name='registration')
]
