"""Admin registrations for the RPG application."""

# Django
from django.contrib import admin

# Local
from .models import Battle, Character, Mission, MissionAttempt, TrainingBot


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'archetype',
        'level',
        'experience',
        'gold',
        'owner',
        'created_at',
    )
    search_fields = ('name', 'archetype', 'owner__username')
    list_filter = ('archetype', 'level')


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty', 'minimum_level', 'experience_reward', 'gold_reward')
    search_fields = ('name',)
    list_filter = ('difficulty',)


@admin.register(MissionAttempt)
class MissionAttemptAdmin(admin.ModelAdmin):
    list_display = ('mission', 'character', 'success', 'experience_earned', 'created_at')
    list_filter = ('success', 'mission__difficulty')
    search_fields = ('mission__name', 'character__name')


@admin.register(TrainingBot)
class TrainingBotAdmin(admin.ModelAdmin):
    list_display = ('name', 'power_rating', 'experience_reward', 'gold_reward')
    search_fields = ('name',)


@admin.register(Battle)
class BattleAdmin(admin.ModelAdmin):
    list_display = (
        'challenger',
        'opponent',
        'bot',
        'winner',
        'is_training',
        'created_at',
    )
    list_filter = ('is_training', 'winner')
    search_fields = ('challenger__name', 'opponent__name', 'bot__name')
