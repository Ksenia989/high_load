# Generated by Django 2.0.1 on 2018-01-11 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sightseens', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='distance',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='location',
            name='id',
            field=models.PositiveIntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='электронная почта'),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.PositiveIntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='visit',
            name='id',
            field=models.PositiveIntegerField(primary_key=True, serialize=False),
        ),
    ]
