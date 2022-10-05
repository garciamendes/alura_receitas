# Django
from django.urls import path

# Local
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout', views.logout, name='logout'),
]
