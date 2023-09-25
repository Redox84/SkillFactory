from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import BaseRegisterForm


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/news/'


class QuitView(TemplateView):
    template_name = 'sign/logout.html'


class AuthorView(LoginRequiredMixin, TemplateView):
    template_name = 'sign/status.html'


