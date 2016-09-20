# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-16 11:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Itemsequiped',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idplayer', models.IntegerField(blank=True, null=True)),
                ('iditem', models.IntegerField(blank=True, null=True)),
                ('context', models.CharField(blank=True, max_length=20, null=True)),
                ('bonuslist', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('part', models.CharField(blank=True, max_length=15, null=True)),
                ('ilvl', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'itemsequiped',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Itemshistoric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idplayer', models.IntegerField(blank=True, null=True)),
                ('iditem', models.IntegerField(blank=True, null=True)),
                ('context', models.CharField(blank=True, max_length=20, null=True)),
                ('bonuslist', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('part', models.CharField(blank=True, max_length=15, null=True)),
                ('ilvl', models.IntegerField(blank=True, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'itemshistoric',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Players',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('realm', models.CharField(blank=True, max_length=20, null=True)),
                ('ilvl', models.IntegerField(blank=True, null=True)),
                ('class_field', models.IntegerField(blank=True, db_column='class', null=True)),
                ('race', models.IntegerField(blank=True, null=True)),
                ('gender', models.IntegerField(blank=True, null=True)),
                ('lvl', models.IntegerField(blank=True, null=True)),
                ('faction', models.IntegerField(blank=True, null=True)),
                ('image', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'players',
                'managed': False,
            },
        ),
    ]