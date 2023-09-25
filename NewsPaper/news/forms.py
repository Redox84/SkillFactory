from django import forms
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


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
