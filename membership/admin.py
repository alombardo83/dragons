from django.contrib import admin
from django.db.models import Max
from django.forms.models import ModelChoiceField

from datetime import datetime

import nested_admin
from nested_admin.formsets import NestedInlineFormSet

from .models import Period, MembershipPeriod, Member


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    search_fields = ['name']


class MembershipPeriodInline(nested_admin.NestedStackedInline):
    model = MembershipPeriod
    extra = 1
    fieldsets = (
        (None, {
            'fields': ('period',)
        }),
        ('plus', {
            'classes': ('collapse',),
            'fields': ('comment',),
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'period':
            now = datetime.today()
            queryset = Period.objects.filter(start_date__lte=now, end_date__gte=now)
            return ModelChoiceField(queryset)
        return super(MembershipPeriodInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class MemberInline(nested_admin.NestedStackedInline):
    inlines = [MembershipPeriodInline, ]
    extra = 0
    model = Member
    readonly_fields = ('member_number',)
