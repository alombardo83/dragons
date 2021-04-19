from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('blog/', include('blog.urls')),
    path('top14/', include('top14.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('gallery/', include('gallery.urls')),
    path('', include('core.urls')),
]

handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'
handler403 = 'core.views.handler403'
