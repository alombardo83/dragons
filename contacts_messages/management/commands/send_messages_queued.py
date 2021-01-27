import os

from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from core.mail import get_connection
from contacts.models import Person
from contacts_messages.models import Message


class Command(BaseCommand):
    help = 'Send mails in queue'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Send mails in queue'))

        emails_to = list(Person.objects.exclude(email__isnull=True).exclude(email__exact='').values('email').distinct())
        emails_to = [e['email'] for e in emails_to]
        self.stdout.write(self.style.SUCCESS('Number of contacts : %s' % len(emails_to)))

        messages = Message.objects.filter(sended=False).all()
        self.stdout.write(self.style.SUCCESS('Number of emails : %s' % len(messages)))

        with get_connection('message') as connection:
            for message in messages:
                m = render_to_string('contacts_messages/message.html', {
                    'content': message.body
                })

                for i in range(0, len(emails_to), 50):
                    try:
                        mail = EmailMultiAlternatives(subject=message.subject, from_email=connection.username,
                                                      bcc=emails_to[i:i+50], connection=connection)
                        for file in message.attachments.all():
                            f = file.attachment
                            mail.attach(os.path.basename(f.name), f.read())
                        mail.attach_alternative(m, 'text/html')
                        mail.send()
                    except Exception as err:
                        self.stderr.write(self.style.ERROR(err))

                message.sended = True
                message.save()

        self.stdout.write(self.style.SUCCESS('Finished'))
