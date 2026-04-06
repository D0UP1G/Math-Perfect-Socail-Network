from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.template.loader import render_to_string

from user.models import CustomUser
from posts.models import PostModel
from .models import NewsPost
from .forms import NewsPostForm


@login_required
def home_view(request):
    from posts.forms import PostForm
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('misc:home')
    else:
        form = PostForm(user=request.user)

    posts_qs = PostModel.objects.select_related('created_by').prefetch_related('likes', 'comments').order_by('-is_pinned', '-id')
    paginator = Paginator(posts_qs, 10)
    posts = paginator.get_page(1)
    return render(request, 'home/index.html', {'posts': posts, 'form': form})


@login_required
def feed_api(request):
    """JSON endpoint для infinite scroll."""
    page = int(request.GET.get('page', 1))
    posts_qs = PostModel.objects.select_related('created_by').prefetch_related('likes', 'comments').order_by('-is_pinned', '-id')
    paginator = Paginator(posts_qs, 10)
    page_obj = paginator.get_page(page)

    items = []
    for post in page_obj:
        items.append({
            'pk': post.pk,
            'title': post.title,
            'is_pinned': post.is_pinned,
            'created': str(post.created),
            'image': post.image.url if post.image else None,
            'author_name': post.created_by.get_full_name() or post.created_by.username,
            'author_username': post.created_by.username,
            'author_avatar': post.created_by.avatar.url if post.created_by.avatar else None,
            'likes_count': post.likes.count(),
            'comments_count': post.comments.count(),
            'user_liked': request.user in post.likes.all(),
        })

    return JsonResponse({
        'items': items,
        'has_next': page_obj.has_next(),
        'next_page': page + 1 if page_obj.has_next() else None,
    })


@login_required
def news_view(request):
    news_qs = NewsPost.objects.filter(is_published=True).select_related('author')
    paginator = Paginator(news_qs, 10)
    news = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'news/index.html', {'news': news})


@login_required
def news_detail_view(request, pk):
    post = get_object_or_404(NewsPost, pk=pk, is_published=True)
    return render(request, 'news/detail.html', {'post': post})


@staff_member_required
def news_create_view(request):
    if request.method == 'POST':
        form = NewsPostForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return redirect('misc:news')
    else:
        form = NewsPostForm()
    return render(request, 'news/create.html', {'form': form})


@staff_member_required
def news_delete_view(request, pk):
    post = get_object_or_404(NewsPost, pk=pk)
    post.delete()
    return redirect('misc:news')


@staff_member_required
def admin_statistics_view(request):
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)

    total_users = CustomUser.objects.count()
    total_posts = PostModel.objects.count()
    total_likes = sum(p.likes.count() for p in PostModel.objects.prefetch_related('likes'))
    new_users_week = CustomUser.objects.filter(date_joined__date__gte=week_ago).count()
    new_posts_week = PostModel.objects.filter(created__gte=week_ago).count()
    top_users = CustomUser.objects.order_by('-score')[:5]
    top_posts = PostModel.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:5]
    pinned_post = PostModel.objects.filter(is_pinned=True).first()

    posts_by_day = list(
        PostModel.objects
        .filter(created__gte=week_ago)
        .values('created')
        .annotate(count=Count('id'))
        .order_by('created')
    )

    context = {
        'total_users': total_users,
        'total_posts': total_posts,
        'total_likes': total_likes,
        'new_users_week': new_users_week,
        'new_posts_week': new_posts_week,
        'top_users': top_users,
        'top_posts': top_posts,
        'pinned_post': pinned_post,
        'posts_by_day': posts_by_day,
    }
    return render(request, 'admin/statistics.html', context)
