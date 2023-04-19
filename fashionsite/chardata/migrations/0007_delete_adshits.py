# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chardata', '0006_auto_20170718_1902'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AdsHits',
        ),
    ]
