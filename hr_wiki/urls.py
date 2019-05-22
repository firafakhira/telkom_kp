from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='wiki-home'),
<<<<<<< HEAD
    path('search/', views.sear, name='wiki-search'),
    path('home2/', views.home2, name='wiki-home2'),
    path('search/', views.sear, name='wiki-search')
=======
    path('home2/', views.home2, name='wiki-home2'),
    path('search/', views.sear, name='wiki-search')

>>>>>>> 88fbc3d8070e1b6d9295b0f403713b93c8780a23
]