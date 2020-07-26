from django.db import models
from django.utils.translation import gettext as _

class Person(models.Model):
    first_name = models.CharField(_('first name'), max_length=50)
    last_name = models.CharField(_('last name'), max_length=50)
    birthdate = models.DateField(_('birthdate'))
    phone = models.CharField(_('phone'), max_length=20)
    email = models.EmailField(_('email'), max_length=150)

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('people')
        def __str__(self):
            return '{} {}'.format(self.first_name, self.last_name)

class Address(models.Model):
    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    field1 = models.CharField(_('field 1'), max_length=38)
    field2 = models.CharField(_('field 2'), max_length=38)
    field3 = models.CharField(_('field 3'), max_length=38)
    postal_code = models.CharField(_('postal code'), max_length=5)
    city = models.CharField(_('city'), max_length=32)

    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('addresses')