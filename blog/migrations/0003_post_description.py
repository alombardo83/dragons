# Generated by Django 3.0.8 on 2020-08-28 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200821_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.CharField(default='', max_length=200, verbose_name='description'),
            preserve_default=False,
        ),
    ]