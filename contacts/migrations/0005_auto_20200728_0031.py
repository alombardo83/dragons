# Generated by Django 3.0.8 on 2020-07-27 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0004_auto_20200728_0024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='field2',
            field=models.CharField(blank=True, max_length=38, null=True, verbose_name='field 2'),
        ),
        migrations.AlterField(
            model_name='address',
            name='field3',
            field=models.CharField(blank=True, max_length=38, null=True, verbose_name='field 3'),
        ),
    ]
