from django import forms
from .models import Post


class NewsForm(forms.ModelForm):

    class Meta:
        model = Post
         # fields = '__all__'	#означает, что Django сам должен пойти в модель и взять все поля, кроме первичного ключа
        fields = [
            'title',
            'categoryPost',
            'content',
        ]


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'title',
            'categoryPost',
            'content'
        ]
