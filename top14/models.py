from django.db import models

class Season(models.Model):
    name = models.CharField('nom', max_length=50, unique=True)
    active = models.BooleanField('active', default=False)
    
    class Meta:
        verbose_name = 'saison'
        verbose_name_plural = 'saisons'

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField('nom', max_length=50, unique=True)
    short_name = models.CharField('sigle', max_length=10)
    penalty_points = models.IntegerField('points de pénalité', default=0)
    active = models.BooleanField('active', default=False)
    last_ranking = models.IntegerField('classement de la saison précédente', default=0)
    
    class Meta:
        verbose_name = 'équipe'
        verbose_name_plural = 'équipes'

    def __str__(self):
        return self.name

ROUNDS = (
    (1, 'Journée 1'),
    (2, 'Journée 2'),
    (3, 'Journée 3'),
    (4, 'Journée 4'),
    (5, 'Journée 5'),
    (6, 'Journée 6'),
    (7, 'Journée 7'),
    (8, 'Journée 8'),
    (9, 'Journée 9'),
    (10, 'Journée 10'),
    (11, 'Journée 11'),
    (12, 'Journée 12'),
    (13, 'Journée 13'),
    (14, 'Journée 14'),
    (15, 'Journée 15'),
    (16, 'Journée 16'),
    (17, 'Journée 17'),
    (18, 'Journée 18'),
    (19, 'Journée 19'),
    (20, 'Journée 20'),
    (21, 'Journée 21'),
    (22, 'Journée 22'),
    (23, 'Journée 23'),
    (24, 'Journée 24'),
    (25, 'Journée 25'),
    (26, 'Journée 26'),
)

class Match(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='matches')
    round = models.IntegerField('journée', choices=ROUNDS, default=1)
    date_time = models.DateTimeField('date et heure')
    played = models.BooleanField('joué', default=False)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    drops1 = models.IntegerField('drops domicile', default=0)
    drops2 = models.IntegerField('drops extérieur', default=0)
    penalties1 = models.IntegerField('pénalités domicile', default=0)
    penalties2 = models.IntegerField('pénalités extérieur', default=0)
    tries1 = models.IntegerField('essais domicile', default=0)
    tries2 = models.IntegerField('essais extérieur', default=0)
    conversions1 = models.IntegerField('transformations domicile', default=0)
    conversions2 = models.IntegerField('transformations extérieur', default=0)
    withdrawn_team1 = models.BooleanField('forfait domicile', default=False)
    withdrawn_team2 = models.BooleanField('forfait extérieur', default=False)

    class Meta:
        verbose_name = 'match'
        verbose_name_plural = 'matchs'

    def __str__(self):
        return '{} - {}'.format(self.team1.name, self.team2.name)
