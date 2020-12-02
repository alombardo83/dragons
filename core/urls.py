from . import views
from django.urls import path

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('sent/', views.ActivationSentView.as_view(), name='activation_sent'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('accounts/profile/', views.profile, name='profile'),
    path('media/<path:path>', views.media_access, name='media_access'),
]
