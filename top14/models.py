from django.db import models
from django.utils.translation import gettext, gettext_lazy as _

class Season(models.Model):
    name = models.CharField(_('name'), max_length=50, unique=True)
    active = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = _('season')
        verbose_name_plural = _('seasons')

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(_('name'), max_length=50, unique=True)
    short_name = models.CharField(_('short_name'), max_length=10)
    penalty_points = models.IntegerField(_('penalty points'), default=0)
    active = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = _('team')
        verbose_name_plural = _('teams')

    def __str__(self):
        return self.name

ROUNDS = (
    (1, _('Round 1')),
    (2, _('Round 2')),
    (3, _('Round 3')),
    (4, _('Round 4')),
    (5, _('Round 5')),
    (6, _('Round 6')),
    (7, _('Round 7')),
    (8, _('Round 8')),
    (9, _('Round 9')),
    (10, _('Round 10')),
    (11, _('Round 11')),
    (12, _('Round 12')),
    (13, _('Round 13')),
    (14, _('Round 14')),
    (15, _('Round 15')),
    (16, _('Round 16')),
    (17, _('Round 17')),
    (18, _('Round 18')),
    (19, _('Round 19')),
    (20, _('Round 20')),
    (21, _('Round 21')),
    (22, _('Round 22')),
    (23, _('Round 23')),
    (24, _('Round 24')),
    (25, _('Round 25')),
    (26, _('Round 26')),
)

class Match(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='matches')
    round = models.IntegerField(_('round'), choices=ROUNDS, default=1)
    date_time = models.DateTimeField(_('date and time'))
    played = models.BooleanField(default=False)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    drops1 = models.IntegerField(_('home drops'), default=0)
    drops2 = models.IntegerField(_('away drops'), default=0)
    penalties1 = models.IntegerField(_('home penalties'), default=0)
    penalties2 = models.IntegerField(_('away penalties'), default=0)
    tries1 = models.IntegerField(_('home tries'), default=0)
    tries2 = models.IntegerField(_('away tries'), default=0)
    conversions1 = models.IntegerField(_('home conversions'), default=0)
    conversions2 = models.IntegerField(_('away conversions'), default=0)
    yellow_cards1 = models.IntegerField(_('home yellow cards'), default=0)
    yellow_cards2 = models.IntegerField(_('away yellow cards'), default=0)
    red_cards1 = models.IntegerField(_('home red cards'), default=0)
    red_cards2 = models.IntegerField(_('away red cards'), default=0)

    class Meta:
        verbose_name = _('match')
        verbose_name_plural = _('matches')

    def __str__(self):
        return '{} - {}'.format(self.team1.name, self.team2.name)