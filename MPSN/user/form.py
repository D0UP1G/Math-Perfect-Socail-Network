from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    # Добавляем поле для условий использования

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'username', 'descriptions')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Удаляем стандартные help_text для паролей
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        
        # Настраиваем атрибуты для каждого поля
        self.fields['first_name'].widget.attrs.update({
            'id': 'register-name',
            'class': 'form-control',
            'placeholder': 'Введите ваше имя',
            'autocomplete': 'given-name'
        })
        
        self.fields['last_name'].widget.attrs.update({
            'id': 'register-name',
            'class': 'form-control',
            'placeholder': 'Введите вашу фамилию',
            'autocomplete': 'family-name'
        })
        
        self.fields['email'].widget.attrs.update({
            'id': 'register-email',
            'class': 'form-control',
            'placeholder': 'Введите email',
            'autocomplete': 'email'
        })
        
        self.fields['username'].widget.attrs.update({
            'id': 'register-username',
            'class': 'form-control',
            'placeholder': 'Введите username',
            'autocomplete': 'username'
        })
        
        self.fields['descriptions'].widget.attrs.update({
            'id': 'register-description',
            'class': 'form-control',
            'placeholder': 'Расскажите о себе',
            'rows': 3  # Для текстовой области
        })
        
        self.fields['password1'].widget.attrs.update({
            'id': 'register-password',
            'class': 'form-control',
            'placeholder': 'Придумайте пароль',
            'autocomplete': 'new-password'
        })
        
        self.fields['password2'].widget.attrs.update({
            'id': 'register-confirm',
            'class': 'form-control',
            'placeholder': 'Повторите пароль',
            'autocomplete': 'new-password'
        })
        
        # Изменяем label для полей
        self.fields['first_name'].label = "Имя"
        self.fields['last_name'].label = "Фамилия"
        self.fields['descriptions'].label = "О себе"
    
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

