from django.db import models
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


class MembershipPeriod(models.Model):
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    comment = models.TextField('commentaire', null=True, blank=True)

    class Meta:
        verbose_name = 'période d\'adhésion'
        verbose_name_plural = 'périodes d\'adhésion'
    
    def __str__(self):
        return '{} - {}'.format(self.member, self.period)
