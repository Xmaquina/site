# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-05 16:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Recebido'), (2, 'Aprovado'), (1, 'Em Andamento'), (3, 'Cancelado'), (4, 'Finalizado com Sucesso'), (5, 'Finalizado com Falha')], default=0, verbose_name='Status')),
                ('sent_at', models.DateField(auto_now=True, verbose_name='Enviado em')),
                ('cad_file', models.FileField(upload_to='', verbose_name='Arquivo STL')),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_by', to=settings.AUTH_USER_MODEL, verbose_name='Aprovado por')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL, verbose_name='Proprietário')),
            ],
            options={
                'verbose_name': 'Solicitação',
                'verbose_name_plural': 'Solicitações',
            },
        ),
    ]
