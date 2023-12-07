from django import forms

from .models import Post, Respon
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class BasicSignupForm(SignupForm):  # помещаем пользователя в группу Авторы сразу при регистрации.

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='Authors')
        basic_group.user_set.add(user)
        # Создание объекта Author
        return user


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(label='Объявление', widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class NewsForm(forms.ModelForm):  # форма создания объявлений
    content = forms.CharField(label='Объявление', widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        #fields = '__all__' #  означает, что Django сам должен пойти в модель и взять все поля, кроме первичного ключа
        fields = [
            'title',
            'categoryP',
            'content',
        ]


class ResponForm(forms.ModelForm):

    class Meta:

        model = Respon
        fields = [
            'content',
        ]
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-text', 'cols': 70, 'rows': 3}),
        }

