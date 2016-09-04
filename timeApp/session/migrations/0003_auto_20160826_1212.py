# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0002_team_createat'),
    ]

    operations = [
        migrations.AddField(
            model_name='temporaluser',
            name='wage',
            field=models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True),
        ),
        migrations.AddField(
            model_name='usersession',
            name='total_salary',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True),
        ),
    ]
