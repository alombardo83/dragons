# Generated by Django 3.1.5 on 2021-01-26 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts_messages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='sended',
            field=models.BooleanField(default=False),
        ),
    ]
