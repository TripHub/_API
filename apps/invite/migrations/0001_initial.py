# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-19 12:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('trip', '0006_trip_tag_line'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('uid', models.CharField(editable=False, max_length=32, unique=True)),
                ('email', models.EmailField(max_length=255)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trip.Trip')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
