from django.urls import path
from .views import (NewsList, NewsDetail, Search, ArticleList, ArticleDetail,
                    NewsEdit, NewsDelete, ArticleEdit, ArticleDelete)
from . import views

app_name = 'news'

urlpatterns = [
    path('news/search/', Search.as_view(), name='search'),  # URL-шаблон Поисковой страницы
    path('news/', NewsList.as_view(), name='news'),  # URL-шаблон для списка новостей
    path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),  # URL-шаблон для полной новости
    path('news/create/', views.NewsCreate.as_view(), name='news_create'),  # URL-шаблон для создания новостей
    path('news/<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),  # URL-шаблон для редактирования новостей
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),  # URL-шаблон для удаления новостей
    path('article/', ArticleList.as_view(), name='article'),  # URL-шаблон для списка статей
    path('article/<int:pk>/', ArticleDetail.as_view(), name='article_detail'),  # URL-шаблон для полной статьи
    path('article/create/', views.ArticleCreate.as_view(), name='articles_create'),  # URL-шаблон для создания статьи
    path('article/<int:pk>/edit/', ArticleEdit.as_view(), name='article_edit'), # URL-шаблон для редактирования статьи
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'), # URL-шаблон для удаления статьи
]