from . import views
from django.urls import path

urlpatterns = [
    path('', views.GalleryList.as_view(), name='gallery_list'),
    path('<slug:slug>/', views.gallery_detail, name='gallery_detail'),
]
