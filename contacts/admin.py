from django.contrib import admin
from .models import Person, Address


class AddressInline(admin.StackedInline):
    model = Address


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'birthdate')
    search_fields = ['last_name']
    inlines = [AddressInline,]