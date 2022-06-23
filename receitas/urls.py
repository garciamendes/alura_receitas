# Django
from django.urls import path

# Local
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('receita/<int:receita_id>', views.receita, name='receita'),
    path('busca/', views.buscar, name='buscar'),
]
