from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.db.models import Max
from django.forms.models import ModelChoiceField
from django.template.loader import render_to_string

from datetime import datetime

from .models import Period, MembershipPeriod, Member, Message, Attachment
from core.mail import get_connection
from contacts.models import Person


class AttachmentInline(admin.StackedInline):
    model = Attachment
    extra = 0


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject',)
    inlines = [AttachmentInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['subject', 'body']
        else:
            return []

    def save_model(self, request, obj, form, change):
        send_email = False
        if not obj.pk:
            send_email = True

        super().save_model(request, obj, form, change)

        if send_email:
            message = render_to_string('membership/message.html', {
                'content': obj.body
            })

            now = datetime.today()
            emails_to = list(Member.objects.filter(membershipperiod__period__start_date__lte=now,
                                                   membershipperiod__period__end_date__gte=now).values(
                'person__email').distinct())
            emails_to = [e['person__email'] for e in emails_to]
            with get_connection('message') as connection:
                from_email = None
                if hasattr(connection, 'username'):
                    from_email = connection.username
                try:
                    mail = EmailMultiAlternatives(subject=obj.subject, from_email=from_email, bcc=emails_to,
                                                  connection=connection)
                    for f in request.FILES.values():
                        mail.attach(f.name, f.read(), f.content_type)
                    mail.attach_alternative(message, 'text/html')
                    mail.send()
                except Exception as err:
                    print(err)


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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'period':
            now = datetime.today()
            queryset = Period.objects.filter(start_date__lte=now, end_date__gte=now)
            return ModelChoiceField(queryset)
        return super(MembershipPeriodInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('member_number', 'get_last_name', 'get_first_name', 'is_active')
    search_fields = ['person__last_name']
    fields = ('person',)
    inlines = [MembershipPeriodInline, ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'person':
            queryset = Person.objects.filter(member__isnull=True)
            return ModelChoiceField(queryset)
        return super(MemberAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            max_member_number = Member.objects.all().aggregate(Max('member_number'))['member_number__max']
            new_max_number = None
            if not max_member_number:
                new_max_number = 1
            else:
                new_max_number = int(max_member_number) + 1
            obj.member_number = '{:0>6}'.format(str(new_max_number))
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('person',)
        return self.readonly_fields

    def get_last_name(self, obj):
        return obj.person.last_name

    def get_first_name(self, obj):
        return obj.person.first_name

    def is_active(self, obj):
        now = datetime.today()
        nb_actived_periods = obj.membershipperiod_set.all().filter(period__start_date__lte=now,
                                                                   period__end_date__gte=now).count()
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
