from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login, name="admin-login"),
    path('home', views.home, name="admin-home"),
    path('add/', views.addKonten, name='admin-add'),
    path('edit/<content_id>', views.editKonten, name='admin-edit'),
    path('delete/<content_id>', views.deleteKonten, name='admin-delete'),
]