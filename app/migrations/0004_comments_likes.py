# Generated by Django 4.2.6 on 2023-10-31 17:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_posts_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='likes',
            field=models.ManyToManyField(related_name='comment_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]