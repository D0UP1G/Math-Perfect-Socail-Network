from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from user.models import CustomUser

@login_required
def leaderboard_view(request):
    users = CustomUser.objects.order_by('-score')
    if len(users) > 10:
        users = users[0:9]

    return render(request, 'leaderboard/index.html', {'users':users})
