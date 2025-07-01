from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')  # + кастомные поля

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
             'id': 'login-email',
             'class': 'form-control',
             'placeholder': 'Введите username'
         })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
             'id': 'login-password',
             'class': 'form-control',
             'placeholder': 'Введите пароль'
         })
     )

