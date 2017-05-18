# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-09 18:50
from __future__ import unicode_literals

from django.db import migrations, models
import request.models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0003_auto_20170509_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='cad_file',
            field=models.FileField(upload_to=request.models.user_directory_path, validators=[request.models.validate_stl_file], verbose_name='Arquivo STL'),
        ),
    ]