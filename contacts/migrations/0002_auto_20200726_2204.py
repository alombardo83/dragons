# Generated by Django 3.0.8 on 2020-07-26 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='birthdate',
            field=models.DateField(verbose_name='birthdate'),
        ),
    ]
