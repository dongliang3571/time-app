# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('session', '0003_usersession_total_minutes'),
    ]

    operations = [
        migrations.AddField(
            model_name='temporaluser',
            name='organization',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='temporaluser',
            name='team',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
    ]
