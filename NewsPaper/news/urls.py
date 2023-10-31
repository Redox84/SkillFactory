from django.urls import path
from django.views.decorators.cache import cache_page
from .views import (NewsList, NewsDetail, Search, ArticleList, ArticleDetail, upgrade_me, subscribe, unsubscribe,
                    NewsEdit, NewsDelete, ArticleEdit, ArticleDelete, ProtectedView, AuthorView, CategoryView)
from . import views

app_name = 'news'

urlpatterns = [
    path('search/', Search.as_view(), name='search'),  # URL-шаблон Поисковой страницы
    path('news/', cache_page(60)(NewsList.as_view()), name='news'),  # URL-шаблон для списка новостей
    path('news/<int:pk>/', cache_page(300)(NewsDetail.as_view()), name='news_detail'),  # URL-шаблон для полной новости
    path('news/create/', views.NewsCreate.as_view(), name='news_create'),  # URL-шаблон для создания новостей
    path('news/<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),  # URL-шаблон для редактирования новостей
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),  # URL-шаблон для удаления новостей
    path('article/', ArticleList.as_view(), name='article'),  # URL-шаблон для списка статей
    path('article/<int:pk>/', ArticleDetail.as_view(), name='article_detail'),  # URL-шаблон для полной статьи
    path('article/create/', views.ArticleCreate.as_view(), name='articles_create'),  # URL-шаблон для создания статьи
    path('article/<int:pk>/edit/', ArticleEdit.as_view(), name='article_edit'), # URL-шаблон для редактирования статьи
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'), # URL-шаблон для удаления статьи
    path('upgrade/', upgrade_me, name='upgrade'),
    path('prodected_page/', ProtectedView.as_view()),  # URL-шаблон страницы после авторизации
    path('status/', AuthorView.as_view()),
    path('category/<int:pk>/', CategoryView.as_view(), name='category_list'),  # URL-шаблон списка категорий
    path('category/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('category/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
]