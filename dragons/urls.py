from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('blog/', include('blog.urls')),
    path('top14/', include('top14.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('gallery/', include('gallery.urls')),
    path('', include('core.urls')),
]