from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.landing, name='wiki-landing'),
    path('home/', views.home, name='wiki-home'),
    path('search/<q>', views.search, name='wiki-search'),
    path('content/<content_id>', views.content, name='wiki-content')
]
