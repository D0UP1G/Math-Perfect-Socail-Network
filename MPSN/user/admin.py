from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
	fields = ('username','first_name', 'last_name','email','descriptions','score','is_superuser', 'is_staff','is_active','date_joined')
	exclude = ('last_login','password', 'groups', 'user_permissions')  # Скрыть поле email

admin.site.register(CustomUser, CustomUserAdmin)

