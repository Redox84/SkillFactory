from django.contrib import admin

from .models import Author, Category, Post, Comment, PostCategory


class CategoryInLine(admin.TabularInline):
    model = PostCategory
    extra = 1


class PostAdmin(admin.ModelAdmin):
    model = Post
    inlines = [CategoryInLine]
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('author', 'title', 'choiceType', 'rating')
    list_filter = ('author', 'title', 'choiceType', 'rating')
    search_fields = ['author', 'title', 'choiceType', 'rating']


class AuthorAdmin(admin.ModelAdmin):
    model = Author
    list_display = ('user', 'ratingAuthor')
    list_filter = ('user', 'ratingAuthor')
    search_fields = ['user', 'ratingAuthor']


class PostCategoryAdmin(admin.ModelAdmin):
    model = PostCategory
    list_display = [field.name for field in PostCategory._meta.get_fields()]
    list_filter = ('postPC', 'categoryPC')
    search_fields = ['postPC', 'categoryPC']


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('textCom', 'user', 'rating')
    list_filter = ('user', 'rating')
    search_fields = ['user', 'rating']


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('id', 'nameCategory')
    list_filter = ['nameCategory']
    search_fields = ['nameCategory']


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
