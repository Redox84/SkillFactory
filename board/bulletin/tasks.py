from datetime import timedelta
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.functions import datetime
from django.template.loader import render_to_string

from .models import Post, Respon


@shared_task
def action_every_week():   # Рассылка раз в неделю
    today = datetime.datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(timeCreate__gte=last_week)
    author_emails = set(posts.values_list('author__email', flat=True))
    html_contecst = render_to_string(
        'mailsub/daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Новости за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=author_emails,
    )

    msg.attach_alternative(html_contecst, 'text/html')
    msg.send()


@shared_task
def mail_respon(pk):  # Рассылка при создании отклика
    respon = Respon.objects.get(pk=pk)
    author = respon.postR.author.email

    html_content = render_to_string(
        'mailsub/respon_created_email.html',
        {
            'text': f'{respon.content}',
            'link': f'{settings.SITE_URL}news/{respon.postR.pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject='Новый отклик на ваше объявление',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[author],
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def mail_respon_ac(pk):  # Рассылка при принятии отклика
    respon = Respon.objects.get(pk=pk)
    author_email = respon.author.email
    html_content = render_to_string(
        'mailsub/respon_accept_email.html',
        {
            'text': f'{respon.postR.title}',
            'link': f'{settings.SITE_URL}news/{respon.postR.pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject='Ваш отклик приняли',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[author_email],
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
