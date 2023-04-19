# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chardata', '0003_auto_20160508_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='char',
            name='created_time',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='char',
            name='modified_time',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
