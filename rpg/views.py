"""Views responsible for orchestrating the RPG experience."""

# Python standard library
import random

# Django
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

# Local
from .forms import CharacterForm, DuelForm, MissionAttemptForm, TrainingBattleForm
from .models import (
    Battle,
    Character,
    Mission,
    MissionAttempt,
    TrainingBot,
    resolve_duel,
    resolve_training,
)


def home(request):
    """Overview of the RPG hub with quick access to all features."""

    latest_characters = Character.objects.order_by('-created_at')[:6]
    recent_battles = (
        Battle.objects.select_related('challenger', 'opponent', 'bot', 'winner')
        .all()[:5]
    )
    missions = Mission.objects.all()
    bots = TrainingBot.objects.all()

    context = {
        'latest_characters': latest_characters,
        'recent_battles': recent_battles,
        'missions': missions,
        'bots': bots,
    }
    return render(request, 'rpg/home.html', context)


def character_list(request):
    characters = Character.objects.all()
    return render(request, 'rpg/character_list.html', {'characters': characters})


def character_create(request):
    if request.method == 'POST':
        form = CharacterForm(request.POST)
        if form.is_valid():
            character = form.save(commit=False)
            if request.user.is_authenticated:
                character.owner = request.user
            character.save()
            messages.success(request, 'Ficha criada com sucesso! Prepare-se para a aventura.')
            return redirect('rpg:character_detail', pk=character.pk)
        messages.error(request, 'Não foi possível criar a ficha. Verifique os dados informados.')
    else:
        form = CharacterForm()
    return render(request, 'rpg/character_form.html', {'form': form})


def character_detail(request, pk):
    character = get_object_or_404(Character, pk=pk)
    battle_history = (
        Battle.objects.select_related('winner', 'opponent', 'bot')
        .filter(Q(challenger=character) | Q(opponent=character))
        .order_by('-created_at')[:10]
    )
    mission_attempts = character.mission_attempts.select_related('mission')[:10]
    return render(
        request,
        'rpg/character_detail.html',
        {
            'character': character,
            'battle_history': battle_history,
            'mission_attempts': mission_attempts,
        },
    )


def start_duel(request):
    if Character.objects.count() < 2:
        messages.info(request, 'Cadastre pelo menos dois personagens para iniciar um duelo.')
        return redirect('rpg:character_create')

    if request.method == 'POST':
        form = DuelForm(request.POST)
        if form.is_valid():
            challenger = form.cleaned_data['challenger']
            opponent = form.cleaned_data['opponent']
            with transaction.atomic():
                result = resolve_duel(challenger, opponent)
                battle = Battle.objects.create(
                    challenger=challenger,
                    opponent=opponent,
                    winner=result.winner,
                    log=result.battle_log,
                )
                if result.winner:
                    xp_reward = 80
                    gold_reward = 45
                    result.winner.gain_rewards(xp_reward, gold_reward)
                    messages.success(
                        request,
                        f"{result.winner.name} recebeu {xp_reward} XP e {gold_reward} moedas pela vitória!",
                    )
                else:
                    for hero in (challenger, opponent):
                        hero.gain_rewards(30, 10)
                    messages.info(
                        request,
                        'O duelo terminou em empate épico! Ambos receberam experiência pelo esforço.',
                    )
            return redirect('rpg:battle_log', pk=battle.pk)
        messages.error(request, 'Não foi possível iniciar o duelo. Revise a ficha selecionada.')
    else:
        form = DuelForm()
    return render(request, 'rpg/battle_form.html', {'form': form})


def battle_log(request, pk):
    battle = get_object_or_404(
        Battle.objects.select_related('challenger', 'opponent', 'bot', 'winner'), pk=pk
    )
    return render(request, 'rpg/battle_detail.html', {'battle': battle})


def mission_list(request):
    missions = Mission.objects.all()
    return render(request, 'rpg/mission_list.html', {'missions': missions})


def attempt_mission(request, pk):
    mission = get_object_or_404(Mission, pk=pk)
    if request.method == 'POST':
        form = MissionAttemptForm(mission, request.POST)
        if form.is_valid():
            character = form.cleaned_data['character']
            chance_bonus = character.attribute_total // 2
            success_threshold = min(95, mission.success_rate + chance_bonus)
            roll = random.randint(1, 100)
            success = roll <= success_threshold
            summary = (
                f"{character.name} tentou a missão com uma chance total de {success_threshold}% (dado {roll})."
                f" Resultado: {'sucesso' if success else 'falha'}."
            )
            xp = mission.experience_reward if success else mission.experience_reward // 4
            gold = mission.gold_reward if success else mission.gold_reward // 4
            with transaction.atomic():
                attempt = MissionAttempt.objects.create(
                    mission=mission,
                    character=character,
                    success=success,
                    summary=summary,
                    experience_earned=xp,
                    gold_earned=gold,
                )
                character.gain_rewards(xp, gold)
            if success:
                messages.success(
                    request,
                    f"Missão concluída! {character.name} ganhou {xp} XP e {gold} moedas.",
                )
            else:
                messages.warning(
                    request,
                    f"A missão falhou, mas {character.name} aprendeu algo e ganhou {xp} XP.",
                )
            return redirect('rpg:mission_result', pk=attempt.pk)
        messages.error(request, 'Selecione um personagem apto para realizar a missão.')
    else:
        form = MissionAttemptForm(mission)
    return render(
        request,
        'rpg/mission_attempt.html',
        {
            'mission': mission,
            'form': form,
        },
    )


def mission_result(request, pk):
    attempt = get_object_or_404(
        MissionAttempt.objects.select_related('mission', 'character'), pk=pk
    )
    return render(request, 'rpg/mission_result.html', {'attempt': attempt})


def training_ground(request):
    if not Character.objects.exists():
        messages.info(request, 'Cadastre um personagem antes de iniciar os treinamentos.')
        return redirect('rpg:character_create')

    if request.method == 'POST':
        form = TrainingBattleForm(request.POST)
        if form.is_valid():
            character = form.cleaned_data['character']
            bot = form.cleaned_data['bot']
            with transaction.atomic():
                result = resolve_training(character, bot)
                battle = Battle.objects.create(
                    challenger=character,
                    opponent=None,
                    bot=bot,
                    is_training=True,
                    winner=result.winner,
                    log=result.battle_log,
                )
                if result.winner == character:
                    character.gain_rewards(bot.experience_reward, bot.gold_reward)
                    messages.success(
                        request,
                        f"Treino concluído! {character.name} ganhou {bot.experience_reward} XP e {bot.gold_reward} moedas.",
                    )
                else:
                    character.gain_rewards(bot.experience_reward // 3, bot.gold_reward // 3)
                    messages.warning(
                        request,
                        'Derrota! Use os ensinamentos para melhorar seus atributos.',
                    )
            return redirect('rpg:battle_log', pk=battle.pk)
        messages.error(request, 'Não foi possível iniciar o treino. Corrija os dados e tente novamente.')
    else:
        form = TrainingBattleForm()
    trainings = TrainingBot.objects.all()
    return render(
        request,
        'rpg/training_ground.html',
        {'form': form, 'trainings': trainings},
    )
