from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout

from .form import *
from .models import CustomUser
from posts.models import PostModel
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('user:profile', username=user.username )
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect('user:profile', username=user.username )
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/register.html', {'form': form})
@login_required()
def logout_view(request):
    logout(request)
    return redirect('user:login')

@login_required()
def profile_view(request, username):
    user = CustomUser.objects.filter(username=username)[0]
    posts = PostModel.objects.filter(created_by=user)
    return render(request, 'profile/index.html', {'user':user, 'request': request, 'posts': posts})