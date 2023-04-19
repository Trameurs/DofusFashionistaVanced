# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chardata', '0004_auto_20160511_1717'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdsHits',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count_hit', models.BigIntegerField(default=0)),
                ('banner_language', models.CharField(max_length=5)),
                ('banner_position', models.CharField(max_length=15)),
                ('day', models.DateField(unique=True)),
            ],
        ),
    ]
