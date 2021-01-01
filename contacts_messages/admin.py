from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from contacts.models import Person
from core.mail import get_connection
from .models import Message, Attachment


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
            message = render_to_string('contacts_messages/message.html', {
                'content': obj.body
            })

            emails_to = list(Person.objects.exclude(email__isnull=True).exclude(email__exact='').values('email').distinct())
            emails_to = [e['email'] for e in emails_to]
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