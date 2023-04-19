# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chardata', '0005_adshits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adshits',
            name='day',
            field=models.DateField(),
        ),
    ]
