# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0004_auto_20160826_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='temporaluser',
            name='full_name',
            field=models.CharField(default='aaa', max_length=50),
            preserve_default=False,
        ),
    ]
