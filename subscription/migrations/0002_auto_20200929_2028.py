# Generated by Django 3.1.1 on 2020-09-29 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='command',
            name='seat',
        ),
        migrations.AddField(
            model_name='command',
            name='rank',
            field=models.IntegerField(default=0, verbose_name='rang'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='command',
            name='seat_number',
            field=models.IntegerField(default=0, verbose_name='numéro de siège'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='command',
            name='tribune',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='subscription.tribune'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Seat',
        ),
    ]