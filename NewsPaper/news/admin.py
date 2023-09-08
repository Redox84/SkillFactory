from django.contrib import admin

# Register your models here.

from .models import Author, Category, Post, Comment, PostCategory


class CategoryInLine(admin.TabularInline):
    model = PostCategory
    extra = 1


class PostAdmin(admin.ModelAdmin):
    model = Post
    inlines = [CategoryInLine,]


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)