from django.core.exceptions import ValidationError
from django.db import models
import datetime

def validate_birthday(value):
    if value > datetime.date.today():
        raise ValidationError('La date de naissance ne peut être postérieure à la date du jour')

class Person(models.Model):
    first_name = models.CharField('prénom', max_length=50)
    last_name = models.CharField('nom', max_length=50)
    birthdate = models.DateField('date de naissance', validators=[validate_birthday])
    phone = models.CharField('téléphone', max_length=20)
    email = models.EmailField('email', max_length=150)

    class Meta:
        verbose_name = 'personne'
        verbose_name_plural = 'personnes'
        unique_together = ('first_name', 'last_name', 'birthdate')

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

class Address(models.Model):
    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    field1 = models.CharField('champ 1', max_length=38)
    field2 = models.CharField('champ 2', max_length=38, null=True, blank=True)
    field3 = models.CharField('champ 3', max_length=38, null=True, blank=True)
    postal_code = models.CharField('code postal', max_length=5)
    city = models.CharField('ville', max_length=32)

    class Meta:
        verbose_name = 'adresse'
        verbose_name_plural = 'adresses'
    
    def __str__(self):
        return '{} {}'.format(self.postal_code, self.city)
