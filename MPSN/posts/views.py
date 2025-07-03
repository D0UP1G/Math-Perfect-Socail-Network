from django.shortcuts import render, redirect
from .forms import PostForm

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
    
    return render(request, 'posts/create.html', {'form': form})
