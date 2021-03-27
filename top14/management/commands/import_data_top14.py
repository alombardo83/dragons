import csv
from datetime import datetime

from django.core.management.base import BaseCommand

from top14.models import Season, Team, Match


class Command(BaseCommand):
    help = 'Import Top14 Data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Import Top14 Data'))

        seasons = {}
        with open('seasons.csv', newline='') as file:
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                try:
                    season = Season.objects.get(id=row['id'])
                    self.stdout.write(self.style.SUCCESS('Season {} already exists'.format(season.name)))
                except:
                    season = Season()
                    season.id = int(row['id'])
                    season.name = row['name']
                    season.active = row['active'] == 't'
                    season.save()
                seasons[row['id']] = season

        teams = {}
        with open('teams.csv', newline='') as file:
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                try:
                    team = Team.objects.get(id=row['id'])
                    self.stdout.write(self.style.SUCCESS('Team {} already exists'.format(team.name)))
                except:
                    team = Team()
                    team.id = int(row['id'])
                    team.name = row['name']
                    team.short_name = row['short_name']
                    team.penalty_points = int(row['penalty_points'])
                    team.active = row['active'] == 't'
                    team.last_ranking = int(row['last_ranking'])
                    team.save()
                teams[row['id']] = team

        with open('matches.csv', newline='') as file:
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                try:
                    match = Match.objects.get(id=row['id'])
                    self.stdout.write(self.style.SUCCESS('Match {} already exists'.format(match.name)))
                except:
                    match = Match()
                    match.id = int(row['id'])
                    match.round = int(row['round'])
                    match.date_time = datetime.fromisoformat(row['date_time'])
                    match.played = row['played'] == 't'
                    match.drops1 = int(row['drops1'])
                    match.drops2 = int(row['drops2'])
                    match.penalties1 = int(row['penalties1'])
                    match.penalties2 = int(row['penalties2'])
                    match.tries1 = int(row['tries1'])
                    match.tries2 = int(row['tries2'])
                    match.conversions1 = int(row['conversions1'])
                    match.conversions2 = int(row['conversions2'])
                    match.season = seasons[row['season_id']]
                    match.team1 = teams[row['team1_id']]
                    match.team2 = teams[row['team2_id']]
                    match.withdrawn_team1 = row['withdrawn_team1'] == 't'
                    match.withdrawn_team2 = row['withdrawn_team2'] == 't'
                    match.save()

        self.stdout.write(self.style.SUCCESS('Finished'))
