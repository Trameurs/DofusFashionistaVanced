# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chardata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemDbVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dump_hash', models.CharField(max_length=255)),
                ('created_time', models.DateField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SolutionCounter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('input_hash', models.BigIntegerField()),
                ('get_count', models.IntegerField(default=0)),
                ('created_time', models.DateField(auto_now_add=True, null=True)),
                ('modified_time', models.DateField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SolutionMemory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('input_hash', models.BigIntegerField()),
                ('input', models.BinaryField()),
                ('stored', models.BinaryField()),
            ],
        ),
        migrations.CreateModel(
            name='SolutionMemoryHits',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count_hit', models.BigIntegerField(default=0)),
                ('count_miss', models.BigIntegerField(default=0)),
                ('day', models.DateField()),
            ],
        ),
        migrations.AlterField(
            model_name='char',
            name='level',
            field=models.IntegerField(),
        ),
    ]
