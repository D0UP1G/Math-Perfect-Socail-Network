from django.db import models
from django.conf import settings


class NewsPost(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Содержание')
    image = models.ImageField('Изображение', upload_to='news/', blank=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='news_posts',
        verbose_name='Автор'
    )
    created = models.DateTimeField('Дата публикации', auto_now_add=True)
    is_published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created']

    def __str__(self):
        return self.title
