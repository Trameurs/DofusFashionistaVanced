# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Char',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_time', models.DateField(auto_now_add=True)),
                ('modified_time', models.DateField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('char_name', models.CharField(max_length=50)),
                ('char_class', models.CharField(max_length=20)),
                ('char_build', models.CharField(max_length=50)),
                ('level', models.IntegerField(max_length=3)),
                ('minimum_stats', models.BinaryField()),
                ('minimum_crits', models.BinaryField()),
                ('stats_weight', models.BinaryField()),
                ('minimal_solution', models.BinaryField(default=b'')),
                ('link_shared', models.BooleanField()),
                ('options', models.BinaryField()),
                ('inclusions', models.BinaryField()),
                ('exclusions', models.BinaryField()),
                ('aspects', models.BinaryField(default=b'')),
                ('deleted', models.BooleanField(default=False)),
                ('allow_points_distribution', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CharBaseStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stat', models.CharField(max_length=30)),
                ('total_value', models.IntegerField(default=0)),
                ('scrolled_value', models.IntegerField(default=0)),
                ('char', models.ForeignKey(to='chardata.Char')),
            ],
        ),
        migrations.CreateModel(
            name='UserAlias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.CharField(max_length=50, null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
    ]
