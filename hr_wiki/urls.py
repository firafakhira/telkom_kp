from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='wiki-home'),
<<<<<<< HEAD
    path('search/', views.sear, name='wiki-search')
    
=======
    path('home2/', views.home2, name='wiki-home2'),
    path('search/', views.sear, name='wiki-search')

>>>>>>> 0b8a0203fee861eb23577fa5851df7e1b4f179fa
]