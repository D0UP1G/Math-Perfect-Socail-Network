from django.urls import path
from .views import (
    home_view, feed_api, news_view, news_detail_view,
    news_create_view, news_delete_view, admin_statistics_view
)

app_name = 'misc'

urlpatterns = [
    path('', home_view, name='home'),
    path('api/feed/', feed_api, name='feed_api'),
    path('news/', news_view, name='news'),
    path('news/<int:pk>/', news_detail_view, name='news_detail'),
    path('news/create/', news_create_view, name='news_create'),
    path('news/<int:pk>/delete/', news_delete_view, name='news_delete'),
    path('statistics/', admin_statistics_view, name='statistics'),
]
