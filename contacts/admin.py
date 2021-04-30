from django.contrib import admin
from datetime import date

import nested_admin
from django_object_actions import DjangoObjectActions
from docxtpl import DocxTemplate

from membership.admin import MemberInline
from membership.models import Member
from subscription.admin import ClientInline
from .models import Person, Address


class AddressInline(nested_admin.NestedStackedInline):
    model = Address


@admin.register(Person)
class PersonAdmin(DjangoObjectActions, nested_admin.NestedModelAdmin):
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

    def generate_summons(self, request, queryset):
        for m in Member.objects.all():
            if m.is_active():
                doc = DocxTemplate("summons_template.docx")
                context = {
                    'generate_date': date.today().strftime('%d %B %Y'),
                    'lastname': m.person.last_name,
                    'firstname': m.person.first_name,
                    'address_line1': m.person.address.field1,
                    'address_line2': m.person.address.field2,
                    'address_line3': m.person.address.field3,
                    'address_postal_code': m.person.address.postal_code,
                    'address_city': m.person.address.city,
                }
                doc.render(context)
                doc.save('summons_{}_{}.docx'.format(m.person.last_name, m.person.first_name))

    generate_summons.label = 'Générer convocations'
    generate_summons.short_description = 'Génère les convocations à l\'assemblée générale'

    changelist_actions = ('generate_summons',)
