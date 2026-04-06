from django.contrib import admin
from django.utils.html import format_html
from .models import PostModel, Comment


@admin.register(PostModel)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created', 'likes_count', 'views', 'is_pinned', 'image_preview', 'pin_action')
    list_filter = ('is_pinned', 'created')
    search_fields = ('title', 'description', 'created_by__username')
    readonly_fields = ('views', 'created', 'image_preview_large')
    list_editable = ('is_pinned',)
    ordering = ('-is_pinned', '-created')
    actions = ['pin_post', 'unpin_post']

    fieldsets = (
        ('Основное', {
            'fields': ('title', 'description', 'image', 'image_preview_large')
        }),
        ('Автор и статус', {
            'fields': ('created_by', 'is_pinned', 'views', 'created')
        }),
    )

    def likes_count(self, obj):
        return obj.likes.count()
    likes_count.short_description = 'Лайки'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;">', obj.image.url)
        return '—'
    image_preview.short_description = 'Фото'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:400px;border-radius:8px;">', obj.image.url)
        return '—'
    image_preview_large.short_description = 'Предпросмотр'

    def pin_action(self, obj):
        if obj.is_pinned:
            return format_html('<span style="color:#1d9bf0;font-weight:bold;">📌 Закреплён</span>')
        return '—'
    pin_action.short_description = 'Статус'

    @admin.action(description='Закрепить выбранные посты')
    def pin_post(self, request, queryset):
        # Снимаем закрепление со всех, потом закрепляем выбранный
        PostModel.objects.update(is_pinned=False)
        queryset.update(is_pinned=True)
        self.message_user(request, f'Закреплён пост.')

    @admin.action(description='Открепить выбранные посты')
    def unpin_post(self, request, queryset):
        queryset.update(is_pinned=False)
        self.message_user(request, 'Посты откреплены.')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'text_short', 'created', 'likes_count', 'is_reply')
    list_filter = ('created',)
    search_fields = ('author__username', 'text', 'post__title')
    readonly_fields = ('created',)

    def text_short(self, obj):
        return obj.text[:60] + ('...' if len(obj.text) > 60 else '')
    text_short.short_description = 'Текст'

    def likes_count(self, obj):
        return obj.likes.count()
    likes_count.short_description = 'Лайки'

    def is_reply(self, obj):
        return '↩ Ответ' if obj.parent_id else '—'
    is_reply.short_description = 'Тип'
