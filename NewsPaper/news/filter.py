import django_filters
from .models import *  # (*) Импорт всех моделей
from django import forms


# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем, должен чем-то напомнить знакомые вам Django дженерики.


class PostFilter(django_filters.FilterSet):
    # поиск по названию
    title = django_filters.CharFilter(field_name='title',
                                      lookup_expr='icontains',
                                      label='Заголовок',
                                      widget=forms.TextInput(attrs={'placeholder': 'Поиск по названию'})
                                      )
    # поиск по автору
    author = django_filters.ModelChoiceFilter(field_name='author',
                                              empty_label='Все авторы',
                                              label='Авторы',
                                              queryset=Author.objects.all()
                                              )
    # поиск по типу
    choiceType = django_filters.ChoiceFilter(field_name='choiceType',
                                             empty_label='Все типы',
                                             label='Тип',
                                             choices=Post.CATEGORY_CHOICES
                                             )
    # поиск по категории
    categoryPost = django_filters.ModelChoiceFilter(field_name='categoryPost',
                                                    empty_label='Все категории',
                                                    label='Категория',
                                                    queryset=Category.objects.all()
                                                    )
    # поиск по дате
    timeCreate = django_filters.DateFilter(field_name='timeCreate',
                                           lookup_expr='gte',
                                           label='Дата',
                                           widget=forms.DateInput(attrs={'type': 'date'})
                                           )

    class Meta:
        # В Meta классе мы должны указать Django модель, в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели будет производиться фильтрация.
        fields = ['choiceType', 'author', 'title', 'categoryPost', 'timeCreate']
