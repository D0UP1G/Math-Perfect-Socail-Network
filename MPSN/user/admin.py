from django.contrib import admin
from django.utils.html import format_html
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'email', 'score', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    readonly_fields = ('date_joined', 'last_login', 'banner_preview', 'avatar_preview')
    ordering = ('-score',)

    fieldsets = (
        ('Основное', {
            'fields': ('username', 'first_name', 'last_name', 'email', 'descriptions')
        }),
        ('Профиль', {
            'fields': ('score', 'birth_date', 'banner_url', 'banner', 'avatar', 'banner_preview')
        }),
        ('Права', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Даты', {
            'fields': ('date_joined', 'last_login')
        }),
    )

    def full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'.strip() or '—'
    full_name.short_description = 'Имя'

    def banner_preview(self, obj):
        if obj.banner:
            return format_html('<img src="{}" style="max-width:400px;border-radius:8px;">', obj.banner.url)
        if obj.banner_url:
            return format_html('<img src="{}" style="max-width:400px;border-radius:8px;">', obj.banner_url)
        return '—'
    banner_preview.short_description = 'Баннер'

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="width:80px;height:80px;border-radius:50%;object-fit:cover;">', obj.avatar.url)
        return '—'
    avatar_preview.short_description = 'Аватар'
