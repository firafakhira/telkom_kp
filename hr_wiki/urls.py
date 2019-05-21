from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='wiki-home'),
    path('search/', views.sear, name='wiki-search')
    
]