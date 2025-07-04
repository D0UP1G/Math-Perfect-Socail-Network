from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'posts'

urlpatterns = [
    path('create/', create_post_view, name='create'),
    path('post/<int:pk>', post_edit_view, name='edit'),
    path('api/<int:pk>/<str:action>', handle_like, name='api'),
    path('post/<int:pk>/donate/', handle_count, name='api_score'),

]
