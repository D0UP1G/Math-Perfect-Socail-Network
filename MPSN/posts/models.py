from django.db import models
from user.models import CustomUser

class PostModel(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=8128)
    views = models.PositiveIntegerField()
    likes = models.PositiveIntegerField()
    created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)    

    def __str__(self):
        return f"{self.pk}"   