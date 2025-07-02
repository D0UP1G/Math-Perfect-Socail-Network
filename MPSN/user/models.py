from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser, models.Model):
    descriptions = models.TextField('Описание профиля', max_length=100, default='я думал, но не придумал...')
    score = models.IntegerField(default=0)
    birth_date = models.DateField('Дата рождения', default='2000-09-12')    
