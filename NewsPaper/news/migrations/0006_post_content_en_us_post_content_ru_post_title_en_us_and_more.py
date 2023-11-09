# Generated by Django 4.1.3 on 2023-11-08 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_category_namecategory_en_us_category_namecategory_ru_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content_en_us',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='content_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='title_en_us',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='post',
            name='title_ru',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
