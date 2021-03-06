# Generated by Django 3.1.3 on 2021-01-04 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0004_auto_20201201_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='beneficiary',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='subscription.client'),
            preserve_default=False,
        ),
    ]
