from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    nameCategory = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.nameCategory}'


class Post(models.Model):  # Объявления
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    timeCreate = models.DateTimeField(auto_now_add=True)
    categoryP = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категория')
    title = models.CharField(max_length=100, unique=True, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Текст')

    def __str__(self):
        return f'{self.title}: {self.timeCreate.strftime("%d-%m-%Y, %H:%M:%S")}, {self.author}'

    def get_absolute_url(self):
        return f'news/{self.id}'  # ССЫЛКА НА ОБЪЯВЛЕНИЯ


class PostCategory(models.Model):
    postPC = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryPC = models.ForeignKey(Category, on_delete=models.CASCADE)


class Respon(models.Model):  # Отклики
    postR = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies', verbose_name='Объявление')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    content = models.CharField(max_length=200, verbose_name='Контент')
    timeR = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False, verbose_name='Принять')

    def __str__(self):
        return f'{self.author}: {self.content}'

