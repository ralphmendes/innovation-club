# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2025-02-02 08:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0007_vote_vote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='vote',
            field=models.IntegerField(choices=[(1, 'Upvote'), (-1, 'Downvote')]),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('post', 'author')]),
        ),
    ]
