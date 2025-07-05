from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


from .forms import PostForm
from .models import PostModel
from user.models import CustomUser


import json 


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

@require_GET
@login_required
def handle_like(request, pk, action):
    post = get_object_or_404(PostModel, id=pk)
    
    if action == '1':  # Лайк
        if request.user not in post.likes.all():
            post.likes.add(request.user)
    elif action == '2':  # Анлайк
        if request.user in post.likes.all():
            post.likes.remove(request.user)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid action'}, status=400)
    
    return JsonResponse({
        'success': True,
        'likes_count': post.likes.count(),
        'is_liked': request.user in post.likes.all()
    })

@login_required
@require_POST
def handle_count(request, pk):
    post = get_object_or_404(PostModel, pk=pk)
    data = json.loads(request.body)
    amount = data.get('amount', 5)

    # Проверка баланса пользователя
    if request.user.score < amount:
        return JsonResponse({
            'success': False,
            'error': 'Недостаточно баллов'
        }, status=400)

    # Обновление балансов
    request.user.score -= amount
    request.user.save()
    
    post.created_by.score += amount
    post.created_by.save()

    # Создание записи о донате (если есть модель Donation)
    # Donation.objects.create(
    #     from_user=request.user,
    #     to_user=post.created_by,
    #     post=post,
    #     amount=amount
    # )

    return JsonResponse({
        'success': True,
        'new_balance': request.user.score
    })
