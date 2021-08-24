import os
import time
from datetime import datetime

from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from core.mail import get_connection
from contacts.models import Person
from contacts_messages.models import Message
from membership.models import MembershipPeriod


def receivers_all():
    return Person.objects.values_list('pk', flat=True).distinct()


def members_only():
    now = datetime.today()
    members = MembershipPeriod.objects.filter(period__start_date__lte=now, period__end_date__gte=now) \
        .values_list('member_id', flat=True).distinct()
    return Person.objects.filter(member__in=members).values_list('pk', flat=True).distinct()


def not_members_only():
    now = datetime.today()
    members = MembershipPeriod.objects.filter(period__start_date__lte=now, period__end_date__gte=now) \
        .values_list('member_id', flat=True).distinct()
    return Person.objects.exclude(member__in=members).values_list('pk', flat=True).distinct()


def subscribers_only():
    return Person.objects.values_list('pk', flat=True).distinct()


def not_subscribers_only():
    return Person.objects.values_list('pk', flat=True).distinct()


class Command(BaseCommand):
    help = 'Send mails in queue'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Send mails in queue'))

        switcher = {
            0: receivers_all,
            1: members_only,
            2: not_members_only,
#            3: subscribers_only,
#            4: not_subscribers_only
        }

        messages = Message.objects.filter(status=0).all()
        self.stdout.write(self.style.SUCCESS('Number of emails : %s' % len(messages)))

        if len(messages) > 0:
            for message in messages:
                message.status = 1
                message.save()

            with get_connection('message') as connection:
                for message in messages:
                    try:
                        ids = switcher.get(message.receivers)
                        emails_to = list(Person.objects.filter(pk__in=ids()).exclude(email__isnull=True)
                                         .exclude(email__exact='').values_list('email', flat=True).distinct())
                        self.stdout.write(self.style.SUCCESS('Number of contacts : %s' % len(emails_to)))

                        m = render_to_string('contacts_messages/message.html', {
                            'content': message.body
                        })

                        files = []
                        for file in message.attachments.all():
                            f = file.attachment
                            files.append((os.path.basename(f.name), f.read()))

                        total = 0
                        for i in range(0, len(emails_to), 50):
                            emails = emails_to[i:i+50]
                            total = total + len(emails)
                            if total > 200:
                                time.sleep(3700)
                                total = len(emails)
                            try:
                                mail = EmailMultiAlternatives(subject=message.subject, from_email=connection.username,
                                                              bcc=emails, connection=connection)

                                mail.attach_alternative(m, 'text/html')
                                for file in files:
                                    mail.attach(*file)
                                mail.send()
                            except Exception as err:
                                self.stderr.write(self.style.ERROR(err))

                        message.status = 2
                    except Exception as err:
                        message.status = 3
                        self.stderr.write(self.style.ERROR(err))
                    message.save()

        self.stdout.write(self.style.SUCCESS('Finished'))
