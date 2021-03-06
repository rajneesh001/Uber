# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-07-10 18:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image_url', models.URLField(null=True)),
                ('phone', models.CharField(error_messages={'unique': 'this phone number already being taken'}, max_length=10, unique=True)),
                ('email', models.EmailField(error_messages={'unique': 'this email already being taken'}, max_length=100, unique=True)),
                ('cab_reg_num', models.CharField(max_length=100)),
                ('lat', models.CharField(max_length=50, null=True)),
                ('long', models.CharField(max_length=50, null=True)),
                ('status', models.CharField(default='AVAILABLE', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_lat', models.CharField(max_length=50)),
                ('start_long', models.CharField(max_length=50)),
                ('dest_lat', models.CharField(max_length=50)),
                ('dest_long', models.CharField(max_length=50)),
                ('start_address', models.CharField(max_length=100)),
                ('end_address', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default='INITIATED', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_lat', models.CharField(max_length=50)),
                ('start_long', models.CharField(max_length=50)),
                ('dest_long', models.CharField(max_length=50)),
                ('dest_lat', models.CharField(max_length=50)),
                ('fare', models.CharField(default=0, max_length=100)),
                ('start_address', models.CharField(max_length=100)),
                ('end_address', models.CharField(max_length=100)),
                ('status', models.CharField(default='ASSIGNED', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('distance', models.CharField(max_length=50, null=True)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='driver_ride', to='cabSharing.Driver')),
            ],
        ),
        migrations.CreateModel(
            name='Rider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image_url', models.URLField(null=True)),
                ('phone', models.CharField(error_messages={'unique': 'this phone number already being taken'}, max_length=10, unique=True)),
                ('email', models.EmailField(error_messages={'unique': 'this email already being taken'}, max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='ride',
            name='rider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rider_ride', to='cabSharing.Rider'),
        ),
        migrations.AddField(
            model_name='request',
            name='rider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rider_request', to='cabSharing.Rider'),
        ),
    ]
