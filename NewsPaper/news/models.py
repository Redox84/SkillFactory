from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse


# Create your models here.


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.IntegerField(default=0)

    def update_rating(self):
        post_sum = self.post_set.aggregate(pr=Coalesce(Sum('rating'), 0))['pr']

        comment_sum = self.user.comment_set.aggregate(cr=Coalesce(Sum('rating'), 0))['cr']

        post_comment_rating = self.post_set.aggregate(pcr=Coalesce(Sum('comment__rating'), 0))['pcr']
        self.ratingAuthor = post_sum * 3 + comment_sum + post_comment_rating
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    nameCategory = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nameCategory


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    news = 'NW'
    article = 'AR'
    CATEGORY_CHOICES = (
        (news, 'Новость'),
        (article, 'Статья'),
    )

    choiceType = models.CharField(max_length=2,
                                  choices=CATEGORY_CHOICES,
                                  default=article)
    timeCreate = models.DateTimeField(auto_now_add=True)
    categoryPost = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.content[0:124] + '...'

    def __str__(self):
        return f'{self.title}: {self.timeCreate.strftime("%d-%m-%Y, %H:%M:%S")}'

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])


class PostCategory(models.Model):
    postPC = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryPC = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    postCom = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    textCom = models.TextField(max_length=200)
    timeCom = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.textCom
