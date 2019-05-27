from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='wiki-home'),
    path('home2/', views.home2, name='wiki-home2'),
    path('search/', views.sear, name='wiki-search'),
    path('content/<content_id>', views.content, name='wiki-content')
]