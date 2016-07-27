# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0004_auto_20160725_2000'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='temporaluser',
            name='is_visitor',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='temporaluser',
            name='team',
            field=models.ForeignKey(blank=True, to='session.Team', null=True),
        ),
    ]
