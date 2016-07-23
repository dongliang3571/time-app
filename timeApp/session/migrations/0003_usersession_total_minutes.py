# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0002_usersession_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersession',
            name='total_minutes',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
