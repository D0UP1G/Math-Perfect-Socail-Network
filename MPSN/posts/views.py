from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator

from .forms import PostForm
from .models import PostModel, Comment

import json


@login_required
def create_post_view(request):
    """Отдельная страница создания поста (для редактирования)."""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('misc:home')
    else:
        form = PostForm(user=request.user)
    return render(request, 'posts/create.html', {'form': form})


@login_required
def post_detail_view(request, pk):
    post = get_object_or_404(PostModel, id=pk)

    # Увеличиваем счётчик просмотров
    PostModel.objects.filter(pk=pk).update(views=post.views + 1)

    # Только корневые комментарии (без parent), с prefetch replies
    comments = post.comments.filter(parent=None).select_related('author').prefetch_related(
        'replies__author', 'replies__likes', 'likes'
    )

    # Обработка нового комментария
    if request.method == 'POST' and request.user.is_authenticated:
        text = request.POST.get('text', '').strip()
        parent_id = request.POST.get('parent_id')
        if text:
            parent = None
            if parent_id:
                parent = Comment.objects.filter(pk=parent_id, post=post).first()
            Comment.objects.create(post=post, author=request.user, text=text, parent=parent)
        return redirect('posts:detail', pk=pk)

    return render(request, 'posts/detail.html', {
        'post': post,
        'comments': comments,
        'user_liked': request.user in post.likes.all(),
    })


@login_required
def post_edit_view(request, pk):
    post = get_object_or_404(PostModel, id=pk)
    if request.user != post.created_by:
        return redirect('posts:detail', pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('posts:detail', pk=pk)
    else:
        form = PostForm(instance=post, user=request.user)
    return render(request, 'posts/create.html', {'form': form, 'post': post})


@require_GET
@login_required
def handle_like(request, pk, action):
    post = get_object_or_404(PostModel, id=pk)
    author = post.created_by

    if action == '1':
        if request.user not in post.likes.all():
            post.likes.add(request.user)
            # +1 балл автору за новый лайк (не себе)
            if author != request.user:
                author.score += 1
                author.save(update_fields=['score'])
    elif action == '2':
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            # -1 балл автору при снятии лайка
            if author != request.user and author.score > 0:
                author.score -= 1
                author.save(update_fields=['score'])
    else:
        return JsonResponse({'success': False}, status=400)

    return JsonResponse({
        'success': True,
        'likes_count': post.likes.count(),
        'is_liked': request.user in post.likes.all()
    })


@login_required
@require_POST
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True
    return JsonResponse({'success': True, 'liked': liked, 'count': comment.likes.count()})


@login_required
@require_POST
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author == request.user or request.user.is_staff:
        comment.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=403)


@login_required
@require_POST
def toggle_pin(request, pk):
    if not request.user.is_staff:
        return JsonResponse({'success': False}, status=403)
    post = get_object_or_404(PostModel, pk=pk)
    if post.is_pinned:
        post.is_pinned = False
        post.save(update_fields=['is_pinned'])
        return JsonResponse({'success': True, 'pinned': False})
    else:
        # Снимаем закрепление со всех остальных
        PostModel.objects.exclude(pk=pk).update(is_pinned=False)
        post.is_pinned = True
        post.save(update_fields=['is_pinned'])
        return JsonResponse({'success': True, 'pinned': True})
