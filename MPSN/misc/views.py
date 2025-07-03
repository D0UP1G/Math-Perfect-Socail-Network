from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from user.models import CustomUser
from posts.models import PostModel

import random


@login_required
def leaderboard_view(request):
    users = CustomUser.objects.order_by('-score')
    if len(users) > 10:
        users = users[0:9]

    return render(request, 'leaderboard/index.html', {'users':users})

@login_required
def home_view(request):
    # Получаем общее количество записей
    count = PostModel.objects.count()
    
    if count > 0:
        # Генерируем случайный индекс
        random_index = random.randint(0, count - 1)
        # Берём запись по индексу
        random_object = PostModel.objects.all()[random_index]
    else:
        random_object = None

    return render(request, 'home/index.html', {'post': random_object, 'request':request})
