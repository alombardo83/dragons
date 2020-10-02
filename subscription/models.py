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

class Tribune(models.Model):
    name = models.CharField('nom', max_length=20, unique=True)
    
    class Meta:
        verbose_name = 'tribune'
        verbose_name_plural = 'tribunes'

    def __str__(self):
        return self.name

class Rate(models.Model):
    name = models.CharField('nom', max_length=20, unique=True)
    
    class Meta:
        verbose_name = 'taux'
        verbose_name_plural = 'taux'

    def __str__(self):
        return self.name

class TribuneRate(models.Model):
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    tribune = models.ForeignKey(Tribune, on_delete=models.CASCADE)
    rate = models.ForeignKey(Rate, on_delete=models.CASCADE)
    price = models.DecimalField('prix', max_digits=5, decimal_places=2)
    
    class Meta:
        unique_together = ('period', 'tribune', 'rate')

class Client(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    client_number = models.CharField('numéro de client', max_length=10, unique=True)

    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'

    def __str__(self):
        return '{} {} ({})'.format(self.person.last_name, self.person.first_name, self.client_number)

COMMAND_TYPE = (
    (1, 'Classique'),
    (2, 'Fidélité')
)

class Command(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='commands')
    command_number = models.CharField('numéro de commande', max_length=10, unique=True)
    tribune = models.ForeignKey(Tribune, on_delete=models.CASCADE, related_name='seats')
    rank = models.IntegerField('rang')
    seat_number = models.IntegerField('numéro de siège')
    rate = models.ForeignKey(Rate, on_delete=models.CASCADE, related_name='commands')
    price = models.DecimalField('prix', max_digits=5, decimal_places=2)
    type = models.IntegerField('type', choices=COMMAND_TYPE, default=1)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'commande'
        verbose_name_plural = 'commandes'

    def __str__(self):
        return '{} {} ({})'.format(self.client.person.last_name, self.client.person.first_name, self.command_number)
