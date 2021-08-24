from datetime import datetime

from django.contrib import admin

import nested_admin

from membership.admin import MemberInline
from membership.models import MembershipPeriod
from subscription.admin import ClientInline
from .models import Person, Address


class MemberActiveFilter(admin.SimpleListFilter):
    title = 'Actif'
    parameter_name = 'active'

    def lookups(self, request, model_admin):
        return (
            (True, 'Oui'),
            (False, 'Non')
        )

    def queryset(self, request, queryset):
        now = datetime.today()
        members = MembershipPeriod.objects.filter(period__start_date__lte=now, period__end_date__gte=now)\
            .values_list('member_id', flat=True).distinct()

        active = self.value()
        if active == 'True':
            return queryset.filter(member__id__in=members)
        elif active == 'False':
            return queryset.exclude(member__id__in=members)
        else:
            return queryset


class AddressInline(nested_admin.NestedStackedInline):
    model = Address


@admin.register(Person)
class PersonAdmin(nested_admin.NestedModelAdmin):
    list_display = ('last_name', 'first_name', 'birthdate', 'member', 'is_active')
    search_fields = ['last_name']
    list_filter = (MemberActiveFilter,)
    inlines = [
        AddressInline,
        MemberInline,
        ClientInline,
    ]

    def is_active(self, obj):
        return obj.member.is_active()

    is_active.short_description = 'Adhésion active'
    is_active.admin_order_field = 'is_active'
    is_active.boolean = True