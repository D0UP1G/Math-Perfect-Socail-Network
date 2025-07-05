from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext_lazy as _

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
    error_messages = {
            'username': {
                'max_length': "Заголовок не должен превышать 128 символов",
                'required': "Пожалуйста, укажите username"
            },
            'password': {
                'max_length': "Текст поста не должен превышать 8128 символов",
                'required': "Пожалуйста, введите пароль"
            }
    }

class CustomUserEditForm(UserChangeForm):
    # Кастомизация полей
    descriptions = forms.CharField(
        label=_('Описание профиля'),
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': _('Расскажите о себе...')
        }),
        max_length=100,
        required=False
    )
    
    birth_date = forms.DateField(
        label=_('Дата рождения'),
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    banner_url = forms.URLField(
        label=_('URL баннера'),
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': _('https://example.com/image.jpg')
        }),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'descriptions',
            'birth_date',
            'banner_url'
        )
        # Исключаем поля пароля и score (так как score не должен редактироваться вручную)
        exclude = ('password', 'score', 'last_login', 'is_superuser', 
                  'is_staff', 'is_active', 'date_joined', 'groups', 
                  'user_permissions')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Дополнительные настройки полей
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        
        # Делаем email обязательным
        self.fields['email'].required = True
