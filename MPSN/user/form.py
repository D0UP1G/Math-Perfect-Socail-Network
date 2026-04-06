from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'username', 'descriptions')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        placeholders = {
            'first_name': 'Введите ваше имя',
            'last_name': 'Введите вашу фамилию',
            'email': 'Введите email',
            'username': 'Введите username',
            'descriptions': 'Расскажите о себе',
            'password1': 'Придумайте пароль',
            'password2': 'Повторите пароль',
        }
        for field, ph in placeholders.items():
            self.fields[field].widget.attrs.update({'class': 'form-control', 'placeholder': ph})
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['descriptions'].label = 'О себе'


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
    )


class CustomUserEditForm(UserChangeForm):
    descriptions = forms.CharField(
        label='О себе',
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Расскажите о себе...'}),
        max_length=300,
        required=False
    )
    birth_date = forms.DateField(
        label='Дата рождения',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    banner_url = forms.URLField(
        label='URL баннера (если нет файла)',
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
        required=False
    )
    banner = forms.ImageField(
        label='Загрузить баннер',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'})
    )
    avatar = forms.ImageField(
        label='Загрузить аватар',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email',
                  'descriptions', 'birth_date', 'banner_url', 'banner', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in ('username', 'first_name', 'last_name', 'email'):
            self.fields[f].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].required = True
        # Убираем поле пароля которое добавляет UserChangeForm
        if 'password' in self.fields:
            del self.fields['password']
