from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


# Create your models here.


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.IntegerField(default=0)

    def update_rating(self):
        post_sum = self.post_set.aggregate(postRating=Sum('rating'))
        temp_sum_p = 0
        temp_sum_p += post_sum.get('postRating')

        comment_sum = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        temp_sum_c = 0
        temp_sum_c += comment_sum.get('commentRating')

        self.ratingAuthor = temp_sum_p * 3 + temp_sum_c
        self.save()


class Category(models.Model):
    nameCategory = models.CharField(max_length=100, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )

    choiceType = models.CharField(max_length=2,
                                  choices=CATEGORY_CHOICES,
                                  default=ARTICLE)
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


class PostCategory(models.Model):
    postPC = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryPC = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    postCom = models.ForeignKey(Post, on_delete=models.CASCADE)
    userC = models.ForeignKey(User, on_delete=models.CASCADE)
    textCom = models.TextField(max_length=200)
    timeCom = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
