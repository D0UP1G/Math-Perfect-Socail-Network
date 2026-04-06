from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout

from .form import LoginForm, CustomUserCreationForm, CustomUserEditForm
from .models import CustomUser
from posts.models import PostModel


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('user:profile', username=user.username)
            return render(request, 'user/login.html', {'form': form, 'errors': 'Неверные логин или пароль'})
        return render(request, 'user/login.html', {'form': form, 'errors': 'Неверные данные'})
    return render(request, 'user/login.html', {'form': LoginForm()})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user:profile', username=user.username)
        return render(request, 'user/register.html', {'form': form})
    return render(request, 'user/register.html', {'form': CustomUserCreationForm()})


@login_required
def logout_view(request):
    logout(request)
    return redirect('user:login')


@login_required
def profile_view(request, username):
    user = get_object_or_404(CustomUser, username=username)
    posts = PostModel.objects.filter(created_by=user).order_by('-id')[:10]
    return render(request, 'profile/index.html', {'user': user, 'posts': posts})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user:profile', username=request.user.username)
    else:
        form = CustomUserEditForm(instance=request.user)
    return render(request, 'profile/edit.html', {'form': form})
