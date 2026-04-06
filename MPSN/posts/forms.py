from django import forms
from .models import PostModel

class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок поста',
                'autocomplete': 'off',
                'maxlength': '128',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Напишите содержание поста',
                'id': 'markdown-editor',
                'rows': 8,
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*',
            }),
        }
        labels = {
            'title': 'Заголовок',
            'description': 'Содержание',
            'image': 'Изображение',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.created_by = self.user
        if not instance.pk:
            instance.views = 0
        if commit:
            instance.save()
        return instance
