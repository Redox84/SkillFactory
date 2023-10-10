from datetime import timedelta
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.functions import datetime
from django.template.loader import render_to_string

from .models import Post, Category


@shared_task
def action_every_week():   # Рассылка раз в неделю
    today = datetime.datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(timeCreate__gte=last_week)
    categoriest = set(posts.values_list('categoryPost__nameCategory', flat=True))
    subscribers = set(
        Category.objects.filter(nameCategory__in=categoriest).values_list('subscribers__email', flat=True)
    )

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
        to=subscribers,
    )

    msg.attach_alternative(html_contecst, 'text/html')
    msg.send()


@shared_task
def mail_task(pk):  # Рассылка при создании поста
    post = Post.objects.get(pk=pk)
    categories = post.categoryPost.all()
    title = post.title
    subscribers_emails = []
    for cat in categories:
        subscribers_users = cat.subscribers.all()
        for sub_user in subscribers_users:
            subscribers_emails.append(sub_user.email)

    html_content = render_to_string(
        'mailsub/post_created_email.html',
        {
            'text': f'{post.title}',
            'link': f'{settings.SITE_URL}news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()