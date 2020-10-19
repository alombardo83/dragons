from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.views import generic
from django.conf import settings

from .forms import SignUpForm, ProfileForm
from .tokens import account_activation_token

class HomePageView(generic.TemplateView):
    template_name = 'core/home.html'

class ActivationSentView(generic.TemplateView):
    template_name = 'registration/activation_sent.html'
    
def profile(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    user = request.user
    data = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'newsletter_subscription': user.profile.newsletter_subscription,
    }

    if request.method  == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.username = form.cleaned_data.get('username')
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.newsletter_subscription = form.cleaned_data.get('newsletter_subscription')
            user.save()
            
            if form.has_changed() and 'email' in form.changed_data:
                # user can't login until link confirmed
                user.is_active = False
                user.save()
                
                current_site = get_current_site(request)
                subject = 'Vérifier votre nouveau courriel'
                # load a template like get_template() 
                # and calls its render() method immediately.
                message = render_to_string('registration/activation_request.html', {
                    'user': user,
                    'protocol': settings.PROTOCOL,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    # method will generate a hash value with user related data
                    'token': account_activation_token.make_token(user),
                })
                with get_connection('registration') as connection:
                    from_email = None
                    if hasattr(connection, 'username'):
                        from_email = connection.username
                    user.email_user(subject, message, connection=connection)
                return redirect('activation_sent')
        else:
            print(form.errors)
    else:
        form = ProfileForm(data, instance=request.user)
    return render(request, 'core/profile.html', {'form': form})
    
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true 
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'registration/activation_invalid.html')

def signup_view(request):
    if request.method  == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.newsletter_subscription = form.cleaned_data.get('newsletter_subscription')
            # user can't login until link confirmed
            user.is_active = False
            user.save()
            
            current_site = get_current_site(request)
            subject = 'Activation de votre compte'
            # load a template like get_template() 
            # and calls its render() method immediately.
            message = render_to_string('registration/activation_request.html', {
                'user': user,
                'protocol': settings.PROTOCOL,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(user),
            })
            with get_connection('registration') as connection:
                from_email = None
                if hasattr(connection, 'username'):
                    from_email = connection.username
                user.email_user(subject, message, connection=connection)
            return redirect('activation_sent')
        else:
            print(form.errors)
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})
