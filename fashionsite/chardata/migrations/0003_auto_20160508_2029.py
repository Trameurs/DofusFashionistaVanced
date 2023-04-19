# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chardata', '0002_auto_20160508_0202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solutioncounter',
            name='input_hash',
            field=models.BigIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='solutionmemory',
            name='input_hash',
            field=models.BigIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='solutionmemoryhits',
            name='day',
            field=models.DateField(unique=True),
        ),
    ]
