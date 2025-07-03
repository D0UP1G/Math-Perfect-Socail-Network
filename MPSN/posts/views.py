from django.shortcuts import render, redirect
from .forms import PostForm
from django.contrib.auth.decorators import login_required

@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, user=request.user)  # Передаем текущего пользователя
        if form.is_valid():
            form.save()
            return redirect('user:profile', username=request.user.username)  # Перенаправляем после успешного создания
        else:
            print(form.errors)
    else:
        form = PostForm(user=request.user)
    
    return render(request, 'posts/create.html', {'form': form, 'request': request})

from django.shortcuts import get_object_or_404
from .models import PostModel


@login_required
def post_edit_view(request, pk=None):
    # Если передан post_id - это редактирование существующего поста
    post = get_object_or_404(PostModel, id=pk)
    if request.user == post.created_by:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post, user=request.user)
            if form.is_valid():
                form.save()
                return redirect('user:profile', username=request.user.username)
            else:
                print(form.errors)
        else:
            form = PostForm(instance=post, user=request.user)
        
        context = {
            'form': form,
            'request':request,
            'post': post,  # Передаем объект поста в шаблон
        }
        return render(request, 'posts/create.html', context)
    else:
        context ={
            'post':post
        }
        return render(request, 'posts/index.html', context )