from django.db import models
from django.utils.translation import gettext as _
from contacts.models import Person

class Period(models.Model):
    name = models.CharField(_('name'), max_length=50, unique=True)
    start_date = models.DateField(_('start date'))
    end_date = models.DateField(_('end date'))
    
    class Meta:
        verbose_name = _('period')
        verbose_name_plural = _('periods')

    def __str__(self):
        return self.name

class Member(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    member_number = models.CharField(_('member number'), max_length=50, unique=True)

    class Meta:
        verbose_name = _('member')
        verbose_name_plural = _('members')

    def __str__(self):
        return '{} {} ({})'.format(self.person.last_name, self.person.first_name, self.member_number)

class MembershipPeriod(models.Model):
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    comment = models.TextField(_('comment'), null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.member, self.period)