from django.contrib import admin
from django.db.models import Max
from .models import Period, MembershipPeriod, Member
from datetime import datetime

@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    search_fields = ['name']

class MembershipPeriodInline(admin.StackedInline):
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

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('member_number', 'get_last_name', 'get_first_name', 'is_active')
    search_fields = ['get_last_name']
    fields = ('person', )
    inlines = [MembershipPeriodInline,]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            max_member_number = Member.objects.all().aggregate(Max('member_number'))['member_number__max']
            new_max_number = None
            if not max_member_number:
                new_max_number = 1
            else:
                new_max_number = int(max_member_number)+1
            obj.member_number = '{:0>6}'.format(str(new_max_number))
        super().save_model(request, obj, form, change)

    def get_last_name(self, obj):
        return obj.person.last_name

    def get_first_name(self, obj):
        return obj.person.first_name

    def is_active(self, obj):
        now = datetime.today()
        nb_actived_periods = obj.membershipperiod_set.all().filter(period__start_date__lte=now, period__end_date__gte=now).count()
        if nb_actived_periods > 0:
            return True
        else:
            return False
    
    get_last_name.short_description = 'Nom'
    get_last_name.admin_order_field = 'person__last_name'
    
    get_first_name.short_description = 'Prénom'
    get_first_name.admin_order_field = 'person__first_name'
    
    is_active.short_description = 'Adhésion active'
    is_active.admin_order_field = 'is_active'
    is_active.boolean = True