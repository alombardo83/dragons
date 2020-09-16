from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, label='Prénom')
    last_name = forms.CharField(max_length=100, label='Nom')
    email = forms.EmailField(max_length=150, label='Email')
    newsletter_subscription = forms.BooleanField(required=False, label='Souscription à la newsletter')

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
