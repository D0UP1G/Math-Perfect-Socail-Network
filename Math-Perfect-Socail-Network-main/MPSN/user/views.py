from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.urls import reverse_lazy
from .form import *
from django.views.generic import FormView, CreateView
from django.contrib.auth import login, authenticate, logout

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                HttpResponse('Not found', status = 400)
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return HttpResponse('Not found', status = 400)
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
