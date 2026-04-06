from django.contrib import admin
from django.utils.html import format_html
from .models import NewsPost

admin.site.site_header = 'Doupig — Панель управления'
admin.site.site_title = 'Doupig Admin'
admin.site.index_title = 'Добро пожаловать в панель управления'


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created', 'is_published', 'image_preview')
    list_filter = ('is_published', 'created')
    search_fields = ('title', 'content', 'author__username')
    list_editable = ('is_published',)
    readonly_fields = ('created', 'image_preview_large')
    ordering = ('-created',)

    fieldsets = (
        ('Содержание', {
            'fields': ('title', 'content', 'image', 'image_preview_large')
        }),
        ('Публикация', {
            'fields': ('author', 'is_published', 'created')
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:36px;border-radius:4px;">', obj.image.url)
        return '—'
    image_preview.short_description = 'Фото'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:400px;border-radius:8px;">', obj.image.url)
        return '—'
    image_preview_large.short_description = 'Предпросмотр'
