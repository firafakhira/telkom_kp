from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='wiki-home'),
    path('home2/', views.home2, name='wiki-home2'),
    path('search/', views.sear, name='wiki-search'),
    path('content/', views.content, name='wiki-content')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)