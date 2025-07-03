from django import forms
from .models import PostModel
from django.utils import timezone
from user.models import CustomUser

class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок поста',
                'id': 'post-title',
                'autocomplete': 'off',
                'type':'text',
                'name':'title',
                'maxlength':'100',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Напишите содержание поста',
                'id': 'markdown-editor',
                'rows': 8,
                'name':"content",
                
            }),
        }
        labels = {
            'title': 'Заголовок',
            'description': 'Содержание'
        }
        error_messages = {
            'title': {
                'max_length': "Заголовок не должен превышать 128 символов",
                'required': "Пожалуйста, укажите заголовок"
            },
            'description': {
                'max_length': "Текст поста не должен превышать 8128 символов",
                'required': "Пожалуйста, напишите содержание поста"
            }
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Получаем пользователя из аргументов
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.created_by = self.user  # Устанавливаем автора
        instance.views = 0  # Инициализируем просмотры
        
        if commit:
            instance.save()
        return instance
