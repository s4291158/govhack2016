# -*- coding: utf-8 -*-
# Generated by Django 1.10b1 on 2016-07-30 06:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('attendence_rate', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Disciplinary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suspension_type', models.CharField(max_length=80)),
                ('num_of_incident', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Naplan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year5_readingmean', models.IntegerField()),
                ('year5_writingmean', models.IntegerField()),
                ('year5_spellingmean', models.IntegerField()),
                ('year5_grammarmean', models.IntegerField()),
                ('year5_numeracymean', models.IntegerField()),
                ('year9_readingmean', models.IntegerField()),
                ('year9_writingmean', models.IntegerField()),
                ('year9_spellingmean', models.IntegerField()),
                ('year9_grammarmean', models.IntegerField()),
                ('year9_numeracymean', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
                ('postcode', models.IntegerField()),
                ('lat', models.FloatField(blank=True, null=True)),
                ('lng', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SecondLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('second_language', models.CharField(max_length=40)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.School')),
            ],
        ),
        migrations.CreateModel(
            name='SubjectEnrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=40)),
                ('year_11_enroll', models.CharField(max_length=40)),
                ('year_12_enroll', models.CharField(max_length=40)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.School')),
            ],
        ),
        migrations.AddField(
            model_name='naplan',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.School'),
        ),
        migrations.AddField(
            model_name='disciplinary',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.School'),
        ),
        migrations.AddField(
            model_name='attendence',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.School'),
        ),
    ]
