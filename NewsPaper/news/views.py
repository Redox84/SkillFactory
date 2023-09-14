from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post,  Category
from .filter import PostFilter
from .forms import NewsForm, ArticleForm
from django.urls import reverse_lazy


#  Новости
class NewsList(ListView):  # список превью
    model = Post
    template_name = 'flatpages/news.html'
    context_object_name = 'news'
    paginate_by = 10    # вот так мы можем указать количество записей на странице

    def get_queryset(self):
        queryset = super().get_queryset().filter(choiceType='NW')  # Фильтруем только новости
        return queryset.order_by('-timeCreate')        # и сортируем по убыванию даты


class NewsDetail(DetailView):  # полные новости
    model = Post
    template_name = 'flatpages/news_detail.html'
    context_object_name = 'post'


# Добавляем новое представление для создания новостей.
class NewsCreate(CreateView):
    model = Post
    form_class = NewsForm
    template_name = 'flatpages/news_create.html'
    success_url = 'news'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.choiceType = 'NW'
        post.author = self.request.user.author
        post.save()
        return super().form_valid(form)


class NewsEdit(UpdateView):
    model = Post
    form_class = NewsForm
    template_name = 'flatpages/news_edit.html'
    success_url = '/news/'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'flatpages/news_delete.html'
    success_url = '/news/'


# ====== Статьи
class ArticleList(ListView):
    model = Post
    template_name = 'flatpages/article.html'
    context_object_name = 'article'
    paginate_by = 10

    def get_queryset(self):
        article = Post.objects.filter(choiceType='AR').order_by('-timeCreate')
        # Фильтруем только статьи и сортируем по убыванию даты (другим способом)
        return article


class ArticleDetail(DetailView):
    model = Post
    template_name = 'flatpages/article_detail.html'
    context_object_name = 'post'


class ArticleCreate(CreateView):
    model = Post
    form_class = ArticleForm
    template_name = 'flatpages/article_create.html'
    success_url = '/article/'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'AR'
        post.author = self.request.user.author
        post.save()
        return super().form_valid(form)


class ArticleEdit(UpdateView):
    model = Post
    form_class = ArticleForm
    template_name = 'flatpages/article_edit.html'
    success_url = '/article/'


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'flatpages/article_delete.html'
    success_url = '/article/'


#  Поиск
class Search(ListView):
    model = Post
    template_name = 'flatpages/search.html'
    context_object_name = 'search'
    filterset_class = PostFilter
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        context['categories'] = Category.objects.all()  # Получение всех категорий
        return context