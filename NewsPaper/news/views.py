
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.http import HttpResponseRedirect

from .models import Post,  Category, Author
from .filter import PostFilter
from .forms import NewsForm, ArticleForm


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
class NewsCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    model = Post
    form_class = NewsForm
    template_name = 'flatpages/news_create.html'
    success_url = '/news/'

    def form_valid(self, form):
        post = form.save(commit=False)

        if not self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/login/')

        post.choiceType = 'NW'
        post.author = self.request.user.author
        post.save()
        return super().form_valid(form)


class NewsEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    model = Post
    form_class = NewsForm
    template_name = 'flatpages/news_edit.html'
    success_url = '/news/'


class NewsDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
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


class ArticleCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    model = Post
    form_class = ArticleForm
    template_name = 'flatpages/article_create.html'
    success_url = '/article/'

    def form_valid(self, form):
        post = form.save(commit=False)

        if not self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/login/')

        post.type = 'AR'
        post.author = self.request.user.author
        post.save()
        return super().form_valid(form)


class ArticleEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    model = Post
    form_class = ArticleForm
    template_name = 'flatpages/article_edit.html'
    success_url = '/article/'


class ArticleDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
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
    ordering = ['-timeCreate']

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        context['categories'] = Category.objects.all()  # Получение всех категорий
        return context


class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'sign/prodected_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(user=user)
    return HttpResponseRedirect('/status/')


class AuthorView(LoginRequiredMixin, TemplateView):
    template_name = 'sign/status.html'


class CategoryView(ListView):
    model = Post
    template_name = 'mailsub/category.html'
    context_object_name = 'cat_view'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categoryPost=self.category).order_by('-timeCreate')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Поздравляем! Вы подписаны на новости категорию '
    return render(request, 'mailsub/subscribe.html', {'category': category, 'message': message})

@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    return redirect(to='/news/')

