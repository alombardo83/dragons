from datetime import datetime

from django.db import models
from django.db.models import Max

from contacts.models import Person


class Period(models.Model):
    name = models.CharField('nom', max_length=50, unique=True)
    start_date = models.DateField('date de début')
    end_date = models.DateField('date de fin')
    
    class Meta:
        verbose_name = 'période'
        verbose_name_plural = 'périodes'

    def __str__(self):
        return self.name


class Member(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    member_number = models.CharField('numéro d\'adhérent', max_length=50, unique=True)

    class Meta:
        verbose_name = 'adhérent'
        verbose_name_plural = 'adhérents'

    def __str__(self):
        return '{} {} ({})'.format(self.person.last_name, self.person.first_name, self.member_number)

    def is_active(self):
        now = datetime.today()
        nb_actived_periods = self.membershipperiod_set.all().filter(period__start_date__lte=now,
                                                                   period__end_date__gte=now).count()
        if nb_actived_periods > 0:
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        if not self.pk:
            max_member_number = Member.objects.all().aggregate(Max('member_number'))['member_number__max']
            if not max_member_number:
                new_max_number = 1
            else:
                new_max_number = int(max_member_number) + 1
            self.member_number = '{:0>6}'.format(str(new_max_number))
        super(Member, self).save(*args, **kwargs)


class MembershipPeriod(models.Model):
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    comment = models.TextField('commentaire', null=True, blank=True)

    class Meta:
        verbose_name = 'période d\'adhésion'
        verbose_name_plural = 'périodes d\'adhésion'
    
    def __str__(self):
        return '{} - {}'.format(self.member, self.period)
