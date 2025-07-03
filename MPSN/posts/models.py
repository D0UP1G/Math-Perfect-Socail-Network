from django.db import models
from user.models import CustomUser
from django.conf import settings

class PostModel(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=8128)
    views = models.PositiveIntegerField()
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='liked_posts',
        blank=True
    )
    created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)    

    def __str__(self):
        return f"{self.pk}"   
