# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0003_auto_20160826_1212'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Team',
            new_name='Department',
        ),
        migrations.RenameField(
            model_name='temporaluser',
            old_name='team',
            new_name='department',
        ),
    ]
