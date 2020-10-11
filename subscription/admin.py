from django import forms
from django.contrib import admin
from django.forms.models import ModelChoiceField
from datetime import datetime
import json

from .models import Period, Tribune, Rate, TribuneRate, Client, Command
from contacts.models import Person

@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    search_fields = ['name']

@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

class TribuneRateInline(admin.StackedInline):
    model = TribuneRate
    extra = 1

@admin.register(Tribune)
class TribuneAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']
    inlines = [TribuneRateInline,]

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_number', 'get_last_name', 'get_first_name')
    search_fields = ['person__last_name']
    fields = ('person', 'client_number', )
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'person':
            queryset = Person.objects.filter(client__isnull=True)
            return ModelChoiceField(queryset)
        return super(MemberAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('person',)
        return self.readonly_fields

    def get_last_name(self, obj):
        return obj.person.last_name

    def get_first_name(self, obj):
        return obj.person.first_name
    
    get_last_name.short_description = 'Nom'
    get_last_name.admin_order_field = 'person__last_name'
    
    get_first_name.short_description = 'Prénom'
    get_first_name.admin_order_field = 'person__first_name'

@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = ('command_number', 'get_last_name', 'get_first_name')
    search_fields = ['client__person__last_name', 'client__person__first_name']
    fields = ('client', 'command_number', 'period', 'type', 'rate', 'tribune', 'rank', 'seat_number', 'price')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = None
        if db_field.name == 'period':
            now = datetime.today()
            queryset = Period.objects.filter(start_date__lte=now, end_date__gte=now)
            field = ModelChoiceField(queryset = queryset)
        else:
            field = super(CommandAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        
        if db_field.name in ['period', 'rate', 'tribune']:
            field.widget = forms.Select(attrs={
                'class': 'selector-price'
            })
        
        return field
    
    def _get_extra_context(self, extra_context=None):
        extra_context = extra_context or {}
        now = datetime.today()
        periods = Period.objects.filter(start_date__lte=now, end_date__gte=now)
        tribunes = Tribune.objects.all()
        
        prices = {}
        for period in periods:
            p = {
                'start_date': period.start_date.isoformat(),
                'end_date': period.end_date.isoformat(),
                'prices': {}
            }
            for tribune in tribunes:
                rates = TribuneRate.objects.filter(period__pk=period.pk, tribune__pk=tribune.pk)
                t = {}
                for rate in rates:
                    t[str(rate.rate.pk)] = {
                        'price': float(rate.price)
                    }
                p['prices'][str(tribune.pk)] = t
            prices[str(period.pk)] = p
        
        extra_context['prices'] = json.dumps(prices)
        return extra_context
    
    def add_view(self, request, form_url='', extra_context=None):
        return super().add_view(
            request, form_url, extra_context=self._get_extra_context(extra_context),
        )
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        return super().change_view(
            request, object_id, form_url, extra_context=self._get_extra_context(extra_context),
        )
    
    def get_last_name(self, obj):
        return obj.client.person.last_name

    def get_first_name(self, obj):
        return obj.client.person.first_name
    
    get_last_name.short_description = 'Nom'
    get_last_name.admin_order_field = 'client__person__last_name'
    
    get_first_name.short_description = 'Prénom'
    get_first_name.admin_order_field = 'client__person__first_name'
