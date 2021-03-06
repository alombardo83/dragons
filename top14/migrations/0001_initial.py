# Generated by Django 3.0.8 on 2020-08-01 21:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='nom')),
            ],
            options={
                'verbose_name': 'season',
                'verbose_name_plural': 'seasons',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='nom')),
                ('short_name', models.CharField(max_length=10, verbose_name='short_name')),
                ('penalty_points', models.IntegerField(default=0, verbose_name='penalty points')),
            ],
            options={
                'verbose_name': 'team',
                'verbose_name_plural': 'teams',
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.IntegerField(choices=[(1, 'Round 1'), (2, 'Round 2'), (3, 'Round 3'), (4, 'Round 4'), (5, 'Round 5'), (6, 'Round 6'), (7, 'Round 7'), (8, 'Round 8'), (9, 'Round 9'), (10, 'Round 10'), (11, 'Round 11'), (12, 'Round 12'), (13, 'Round 13'), (14, 'Round 14'), (15, 'Round 15'), (16, 'Round 16'), (17, 'Round 17'), (18, 'Round 18'), (19, 'Round 19'), (20, 'Round 20'), (21, 'Round 21'), (22, 'Round 22'), (23, 'Round 23'), (24, 'Round 24'), (25, 'Round 25'), (26, 'Round 26')], default=1, verbose_name='round')),
                ('date_time', models.DateTimeField(verbose_name='date and time')),
                ('played', models.BooleanField(default=False)),
                ('drops1', models.IntegerField(default=0, verbose_name='home drops')),
                ('drops2', models.IntegerField(default=0, verbose_name='away drops')),
                ('penalties1', models.IntegerField(default=0, verbose_name='home penalties')),
                ('penalties2', models.IntegerField(default=0, verbose_name='away penalties')),
                ('tries1', models.IntegerField(default=0, verbose_name='home tries')),
                ('tries2', models.IntegerField(default=0, verbose_name='away tries')),
                ('conversions1', models.IntegerField(default=0, verbose_name='home conversions')),
                ('conversions2', models.IntegerField(default=0, verbose_name='away conversions')),
                ('yellow_cards1', models.IntegerField(default=0, verbose_name='home yellow cards')),
                ('yellow_cards2', models.IntegerField(default=0, verbose_name='away yellow cards')),
                ('red_cards1', models.IntegerField(default=0, verbose_name='home red cards')),
                ('red_cards2', models.IntegerField(default=0, verbose_name='away red cards')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='top14.Season')),
                ('team1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_matches', to='top14.Team')),
                ('team2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_matches', to='top14.Team')),
            ],
            options={
                'verbose_name': 'match',
                'verbose_name_plural': 'matches',
            },
        ),
    ]
