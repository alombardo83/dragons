from django import forms
from django.core.exceptions import ValidationError
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm

from core.mail import get_connection
from core.models import Profile


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, label='Prénom')
    last_name = forms.CharField(max_length=100, label='Nom')
    email = forms.EmailField(max_length=150, label='Email')
    newsletter_subscription = forms.BooleanField(required=False, label='Souscription à la newsletter')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email déjà existant")
        return email

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'newsletter_subscription')


class ProfileForm(UserChangeForm):
    first_name = forms.CharField(max_length=100, label='Prénom')
    last_name = forms.CharField(max_length=100, label='Nom')
    email = forms.EmailField(max_length=150, label='Email')
    newsletter_subscription = forms.BooleanField(required=False, label='Souscription à la newsletter')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'newsletter_subscription')


class PasswordResetWithCustomEmailForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        with get_connection('registration') as connection:
            if hasattr(connection, 'username'):
                from_email = connection.username
            email_message = EmailMultiAlternatives(subject, body, from_email, [to_email], connection=connection)
            if html_email_template_name is not None:
                html_email = loader.render_to_string(html_email_template_name, context)
                email_message.attach_alternative(html_email, 'text/html')

            email_message.send()
