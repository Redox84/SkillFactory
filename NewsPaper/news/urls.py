from django.urls import path
from .views import NewsList, NewsDetail

app_name = 'news'

urlpatterns = [
    path('news/', NewsList.as_view(), name='news'),  # URL-шаблон для списка новостей
    path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),  # URL-шаблон для новостей полностью
]