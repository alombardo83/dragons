# Generated by Django 3.1.1 on 2020-09-28 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contacts', '0007_auto_20200919_1300'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_number', models.CharField(max_length=10, unique=True, verbose_name='numéro de client')),
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='contacts.person')),
            ],
            options={
                'verbose_name': 'client',
                'verbose_name_plural': 'clients',
            },
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='nom')),
                ('start_date', models.DateField(verbose_name='date de début')),
                ('end_date', models.DateField(verbose_name='date de fin')),
            ],
            options={
                'verbose_name': 'période',
                'verbose_name_plural': 'périodes',
            },
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='nom')),
            ],
            options={
                'verbose_name': 'taux',
                'verbose_name_plural': 'taux',
            },
        ),
        migrations.CreateModel(
            name='Tribune',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='nom')),
            ],
            options={
                'verbose_name': 'tribune',
                'verbose_name_plural': 'tribunes',
            },
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField(verbose_name='rang')),
                ('seat_number', models.IntegerField(verbose_name='numéro de siège')),
                ('tribune', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='subscription.tribune')),
            ],
            options={
                'verbose_name': 'siège',
                'verbose_name_plural': 'sièges',
            },
        ),
        migrations.CreateModel(
            name='Command',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('command_number', models.CharField(max_length=10, unique=True, verbose_name='numéro de commande')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='prix')),
                ('type', models.IntegerField(choices=[(1, 'Classique'), (2, 'Fidélité')], default=1, verbose_name='type')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commands', to='subscription.client')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscription.period')),
                ('rate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commands', to='subscription.rate')),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commands', to='subscription.seat')),
            ],
            options={
                'verbose_name': 'commande',
                'verbose_name_plural': 'commandes',
            },
        ),
        migrations.CreateModel(
            name='TribuneRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='prix')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscription.period')),
                ('rate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscription.rate')),
                ('tribune', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscription.tribune')),
            ],
            options={
                'unique_together': {('period', 'tribune', 'rate')},
            },
        ),
    ]
