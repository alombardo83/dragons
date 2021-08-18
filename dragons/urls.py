from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from core.forms import PasswordResetWithCustomEmailForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/password_reset/", auth_views.PasswordResetView.as_view(form_class=PasswordResetWithCustomEmailForm)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('captcha/', include('captcha.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('blog/', include('blog.urls')),
    path('top14/', include('top14.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('gallery/', include('photologue.urls')),
    path('', include('core.urls')),
]

handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'
handler403 = 'core.views.handler403'
