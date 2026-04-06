from django.db import models
from django.conf import settings
from user.models import CustomUser


class PostModel(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=8128)
    image = models.ImageField(upload_to='posts/', blank=True, null=True, verbose_name='Изображение')
    views = models.PositiveIntegerField(default=0)
    is_pinned = models.BooleanField(default=False, verbose_name='Закреплён')
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_posts',
        blank=True
    )
    created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-is_pinned', '-id']

    def __str__(self):
        return self.title

    def comment_count(self):
        return self.comments.count()


class Comment(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    text = models.TextField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments', blank=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created']

    def __str__(self):
        return f'{self.author.username}: {self.text[:40]}'
