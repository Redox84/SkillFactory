from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .tasks import *
from .models import *
from .filter import PostFilters
from .forms import NewsForm, ResponForm


#  Объявления
class NewsList(ListView):
    model = Post
    template_name = 'flatpages/news.html'
    context_object_name = 'news'
    paginate_by = 10    # количество записей на странице

    def get_queryset(self):
        news = Post.objects.order_by('-timeCreate')  # сортируем по убыванию даты
        return news

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Detail(DetailView):  # подробно
    model = Post
    template_name = 'flatpages/detail.html'
    context_object_name = 'post'


# создание объявления.
class Create(LoginRequiredMixin, CreateView):
    model = Post
    form_class = NewsForm
    template_name = 'flatpages/create.html'
    success_url = '/news/'

    def form_valid(self, form):
        post = form.save(commit=False)
        form.instance.author = self.request.user
        post.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# редактирование
class Edit(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = NewsForm
    template_name = 'flatpages/edit.html'
    success_url = '/news/'


# удаление
class Delete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'flatpages/delete.html'
    success_url = '/news/'


# фильтрация объявлений по категориям
class CategoryView(ListView):
    model = Post
    template_name = 'flatpages/category.html'
    context_object_name = 'cat_view'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categoryP=self.category).order_by('-timeCreate')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


# Личный кабинет
class ProtectedView(LoginRequiredMixin, ListView):
    model = Respon
    template_name = 'sign/prodected_page.html'
    context_object_name = 'respon'

    def get_queryset(self, *args):
        queryset = Respon.objects.filter(postR__author_id=self.request.user.id)
        self.filterset = PostFilters(self.request.GET, queryset, request=self.request.user.id)
        if self.request.GET:
            return self.filterset.qs
        return Respon.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


# Отклик
class ResponDetail(DetailView):
    model = Respon
    template_name = 'flatpages/respond.html'
    context_object_name = 'respon'


# Принятие отклика
def respon_accept(request, pk):
    respon = get_object_or_404(Respon, id=pk)
    respon.confirmed = True
    respon.save()
    mail_respon_ac.delay(respon.pk)
    return redirect('/prodected_page/')


# создание отклика
class ResponCreate(LoginRequiredMixin, CreateView):
    model = Respon
    form_class = ResponForm
    template_name = 'flatpages/respon_create.html'
    success_url = '/news/'

    def form_valid(self, form):
        respon = form.save(commit=False)
        form.instance.author = self.request.user
        respon.postR_id = self.kwargs['pk']
        respon.save()
        mail_respon.delay(respon.pk)  # рассылка через рэдис
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# удаление (отклонение) отклика
class ResponDelete(LoginRequiredMixin, DeleteView):
    model = Respon
    template_name = 'flatpages/respon_del.html'
    success_url = '/prodected_page/'



