# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='TemporalUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name=b'email address')),
                ('qr_code_string', models.CharField(max_length=300, null=True, blank=True)),
                ('pin_number', models.CharField(max_length=4, null=True, blank=True)),
                ('is_visitor', models.BooleanField(default=False)),
                ('createAt', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date joined')),
                ('organization', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('team', models.ForeignKey(blank=True, to='session.Team', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('login_time', models.DateTimeField(null=True, verbose_name=b'date time logged in', blank=True)),
                ('logout_time', models.DateTimeField(null=True, verbose_name=b'date time logged out', blank=True)),
                ('is_active', models.BooleanField(default=False, verbose_name=b'check if session is active')),
                ('total_minutes', models.IntegerField(default=0, null=True, blank=True)),
                ('createAt', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date created')),
                ('temporal_user', models.ForeignKey(to='session.TemporalUser')),
            ],
        ),
    ]
