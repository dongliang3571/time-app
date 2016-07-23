# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersession',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name=b'check if session is active'),
        ),
    ]
