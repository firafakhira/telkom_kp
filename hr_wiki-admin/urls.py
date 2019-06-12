from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login, name="admin-login"),
    path('home', views.home, name="admin-home"),
    path('edit/<content_id>', views.editKonten, name='admin-edit')
]