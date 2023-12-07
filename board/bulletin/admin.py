from django.contrib import admin

from .forms import PostAdminForm
from .models import Category, Post, PostCategory, Respon


# импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)
class CategoryInLine(admin.TabularInline):
    model = PostCategory
    extra = 1


class PostAdmin(admin.ModelAdmin):
    model = Post
    form = PostAdminForm
    inlines = (CategoryInLine,)
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('author', 'title', )
    list_filter = ('author', 'title', )
    search_fields = ['author', 'title', ]


class PostCategoryAdmin(admin.ModelAdmin):
    model = PostCategory
    list_display = [field.name for field in PostCategory._meta.get_fields()]
    list_filter = ('postPC', 'categoryPC')
    search_fields = ['postPC', 'categoryPC']


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('id', 'nameCategory')
    list_filter = ['nameCategory']
    search_fields = ['nameCategory']


class ResponAdmin(admin.ModelAdmin):
    model = Respon
    list_display = ('id', 'timeR', )


admin.site.register(Category, CategoryAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Respon, ResponAdmin)




