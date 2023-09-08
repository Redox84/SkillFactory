from django.shortcuts import render
# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Post



#  Новости
class NewsList(ListView):  #список превью
    model = Post
    template_name = 'flatpages/news.html'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = super().get_queryset().filter(choiceType='NW')  # Фильтруем только новости
        return queryset.order_by('-timeCreate')        # и сортируем по убыванию даты


class NewsDetail(DetailView):  #полные новости
    model = Post
    template_name = 'flatpages/news_detail.html'
    context_object_name = 'post'
