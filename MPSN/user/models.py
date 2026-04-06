from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser, models.Model):
    descriptions = models.TextField('Описание профиля', max_length=300, default='я думал, но не придумал...')
    score = models.IntegerField(default=0)
    birth_date = models.DateField('Дата рождения', default='2000-09-12')
    banner_url = models.URLField(blank=True, default='')
    banner = models.ImageField(upload_to='banners/', blank=True, null=True, verbose_name='Баннер')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')

    def get_banner(self):
        """Возвращает баннер: сначала загруженный файл, потом URL, потом None."""
        if self.banner:
            return self.banner.url
        if self.banner_url:
            return self.banner_url
        return None

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        return None
