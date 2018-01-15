# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-10 06:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='\u79f0\u547c')),
                ('content', models.CharField(max_length=240, verbose_name='\u5185\u5bb9')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Comment', verbose_name='\u56de\u590d\u8bc4\u8bba')),
            ],
        ),
    ]
