from django.contrib import admin

import nested_admin

from membership.admin import MemberInline
from subscription.admin import ClientInline
from .models import Person, Address


class AddressInline(nested_admin.NestedStackedInline):
    model = Address


@admin.register(Person)
class PersonAdmin(nested_admin.NestedModelAdmin):
    list_display = ('last_name', 'first_name', 'birthdate', 'is_active')
    search_fields = ['last_name']
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