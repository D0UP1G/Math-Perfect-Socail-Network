from django import forms
from .models import NewsPost


class NewsPostForm(forms.ModelForm):
    class Meta:
        model = NewsPost
        fields = ['title', 'content', 'image', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок новости',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст новости...',
                'rows': 8,
                'id': 'news-editor',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*',
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
            'image': 'Изображение',
            'is_published': 'Опубликовать сразу',
        }
