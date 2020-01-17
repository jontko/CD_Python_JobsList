# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-10-23 16:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=225)),
                ('description', models.CharField(max_length=225)),
                ('location', models.CharField(max_length=225)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips', to='main.User')),
            ],
        ),
        migrations.RemoveField(
            model_name='trip',
            name='user',
        ),
        migrations.DeleteModel(
            name='Trip',
        ),
    ]
