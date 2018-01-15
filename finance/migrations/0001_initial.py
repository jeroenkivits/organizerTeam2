# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-10 16:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('catogory', models.CharField(choices=[('Allowance', 'Allowance'), ('Salary', 'Salary'), ('Cash', 'Cash'), ('Bonus', 'Bonus'), ('Other', 'Other')], max_length=100)),
                ('amount', models.IntegerField()),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
