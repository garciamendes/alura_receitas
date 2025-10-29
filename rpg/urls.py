"""URL routing for the RPG features."""

# Django
from django.urls import path

# Local
from . import views

app_name = 'rpg'

urlpatterns = [
    path('', views.home, name='home'),
    path('fichas/', views.character_list, name='character_list'),
    path('fichas/nova/', views.character_create, name='character_create'),
    path('fichas/<int:pk>/', views.character_detail, name='character_detail'),
    path('duelos/', views.start_duel, name='start_duel'),
    path('batalhas/<int:pk>/', views.battle_log, name='battle_log'),
    path('missoes/', views.mission_list, name='mission_list'),
    path('missoes/<int:pk>/tentar/', views.attempt_mission, name='attempt_mission'),
    path('missoes/resultados/<int:pk>/', views.mission_result, name='mission_result'),
    path('treinos/', views.training_ground, name='training_ground'),
]
