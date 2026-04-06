from django.urls import path
from .views import (
    create_post_view, post_detail_view, post_edit_view,
    handle_like, like_comment, delete_comment, toggle_pin
)

app_name = 'posts'

urlpatterns = [
    path('create/', create_post_view, name='create'),
    path('post/<int:pk>/', post_detail_view, name='detail'),
    path('post/<int:pk>/edit/', post_edit_view, name='edit'),
    path('api/<int:pk>/<str:action>/', handle_like, name='api'),
    path('api/comment/<int:pk>/like/', like_comment, name='comment_like'),
    path('api/comment/<int:pk>/delete/', delete_comment, name='comment_delete'),
    path('api/post/<int:pk>/pin/', toggle_pin, name='pin'),
]
