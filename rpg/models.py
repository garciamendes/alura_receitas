"""Domain models for the browser based table-top RPG experience."""

# Python standard library
from __future__ import annotations
import math
import random
from dataclasses import dataclass

# Django
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Character(models.Model):
    """Represents the hero sheet created by a player."""

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='rpg_characters',
        help_text='Usuário responsável pela ficha, quando autenticado.',
    )
    name = models.CharField('Nome', max_length=120)
    concept = models.CharField(
        'Conceito', max_length=120, help_text='Resumo rápido do personagem.'
    )
    origin = models.CharField(
        'Origem', max_length=120, blank=True, help_text='Cidade, clã ou organização.'
    )
    archetype = models.CharField(
        'Arquétipo', max_length=80, help_text='Classe ou função dentro do grupo.'
    )
    strength = models.PositiveIntegerField('Força', default=1)
    agility = models.PositiveIntegerField('Agilidade', default=1)
    intellect = models.PositiveIntegerField('Intelecto', default=1)
    spirit = models.PositiveIntegerField('Espírito', default=1)
    vitality = models.PositiveIntegerField('Vitalidade', default=1)
    experience = models.PositiveIntegerField('Experiência', default=0)
    gold = models.PositiveIntegerField('Ouro', default=0)
    level = models.PositiveIntegerField('Nível', default=1)
    hit_points = models.PositiveIntegerField('Pontos de Vida', default=10)
    mana = models.PositiveIntegerField('Mana', default=5)
    biography = models.TextField(
        'História', blank=True, help_text='Um pouco sobre as motivações do herói.'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Personagem'
        verbose_name_plural = 'Personagens'

    def __str__(self) -> str:
        return self.name

    @property
    def attribute_total(self) -> int:
        return self.strength + self.agility + self.intellect + self.spirit + self.vitality

    @property
    def combat_power(self) -> int:
        base = self.attribute_total + (self.level * 3)
        return base + self.hit_points + self.mana

    def gain_rewards(self, xp: int, gold: int) -> None:
        self.experience = models.F('experience') + xp
        self.gold = models.F('gold') + gold
        self.save(update_fields=['experience', 'gold'])
        self.refresh_from_db(fields=['experience', 'gold'])
        self.recalculate_level()

    def recalculate_level(self, *, auto_save: bool = True) -> None:
        new_level = max(1, math.floor(self.experience / 100) + 1)
        if new_level != self.level:
            self.level = new_level
            if auto_save and self.pk:
                self.save(update_fields=['level'])


class Mission(models.Model):
    """Story driven activities that characters can tackle for rewards."""

    DIFFICULTY_CHOICES = (
        ('easy', 'Fácil'),
        ('standard', 'Normal'),
        ('heroic', 'Heróica'),
        ('legendary', 'Lendária'),
    )

    name = models.CharField('Nome', max_length=140)
    description = models.TextField('Descrição')
    difficulty = models.CharField(
        'Dificuldade', max_length=12, choices=DIFFICULTY_CHOICES, default='standard'
    )
    minimum_level = models.PositiveIntegerField('Nível mínimo', default=1)
    success_rate = models.PositiveIntegerField(
        'Chance de sucesso (%)', default=70, help_text='Probabilidade base antes de bônus.'
    )
    experience_reward = models.PositiveIntegerField('Experiência', default=50)
    gold_reward = models.PositiveIntegerField('Ouro', default=30)

    class Meta:
        ordering = ['minimum_level', 'name']
        verbose_name = 'Missão'
        verbose_name_plural = 'Missões'

    def __str__(self) -> str:
        return self.name


class MissionAttempt(models.Model):
    """Keeps track of mission outcomes for characters."""

    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='attempts')
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name='mission_attempts'
    )
    success = models.BooleanField('Sucesso', default=False)
    summary = models.TextField('Resumo')
    experience_earned = models.PositiveIntegerField('Experiência recebida', default=0)
    gold_earned = models.PositiveIntegerField('Ouro recebido', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Conclusão de missão'
        verbose_name_plural = 'Conclusões de missão'

    def __str__(self) -> str:
        result = 'sucesso' if self.success else 'falha'
        return f"{self.character} em {self.mission} ({result})"


class TrainingBot(models.Model):
    """NPC opponents used for practice sessions."""

    name = models.CharField('Nome', max_length=120)
    description = models.TextField('Descrição')
    power_rating = models.PositiveIntegerField('Nível de poder', default=5)
    experience_reward = models.PositiveIntegerField('Experiência', default=20)
    gold_reward = models.PositiveIntegerField('Ouro', default=10)

    class Meta:
        ordering = ['power_rating']
        verbose_name = 'Autômato de treino'
        verbose_name_plural = 'Autômatos de treino'

    def __str__(self) -> str:
        return self.name


class Battle(models.Model):
    """Represents both PVP and training encounters."""

    challenger = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name='battles_as_challenger'
    )
    opponent = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='battles_as_opponent',
        null=True,
        blank=True,
    )
    bot = models.ForeignKey(
        TrainingBot,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='battles',
    )
    winner = models.ForeignKey(
        Character,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='battles_won',
    )
    log = models.TextField('Relato da batalha')
    created_at = models.DateTimeField(auto_now_add=True)
    is_training = models.BooleanField('Treino', default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Batalha'
        verbose_name_plural = 'Batalhas'

    def __str__(self) -> str:
        target = self.bot if self.is_training else self.opponent
        return f"{self.challenger} vs {target}"


@dataclass
class BattleResult:
    winner: Character | None
    loser: Character | None
    battle_log: str
    challenger_roll: int
    opponent_roll: int


def resolve_duel(challenger: Character, opponent: Character) -> BattleResult:
    """Simple combat resolution between two characters."""

    challenger_power = challenger.combat_power
    opponent_power = opponent.combat_power
    challenger_roll = random.randint(1, 20) + challenger_power
    opponent_roll = random.randint(1, 20) + opponent_power

    if challenger_roll == opponent_roll:
        log = (
            f"Ambos os heróis travam um duelo equilibrado! "
            f"Empate técnico com {challenger_roll} pontos."
        )
        return BattleResult(None, None, log, challenger_roll, opponent_roll)

    if challenger_roll > opponent_roll:
        log = (
            f"{challenger.name} supera {opponent.name} com {challenger_roll} contra {opponent_roll}. "
            "O campeão celebra a vitória!"
        )
        return BattleResult(challenger, opponent, log, challenger_roll, opponent_roll)

    log = (
        f"{opponent.name} domina o campo ao alcançar {opponent_roll} pontos, "
        f"superando {challenger.name}. Vitória incontestável!"
    )
    return BattleResult(opponent, challenger, log, challenger_roll, opponent_roll)


def resolve_training(challenger: Character, bot: TrainingBot) -> BattleResult:
    """Combat resolution versus an automated training bot."""

    challenger_power = challenger.combat_power
    bot_power = bot.power_rating * 8
    challenger_roll = random.randint(1, 20) + challenger_power
    opponent_roll = random.randint(1, 20) + bot_power

    if challenger_roll >= opponent_roll:
        log = (
            f"{challenger.name} vence o autômato {bot.name}! "
            f"{challenger_roll} contra {opponent_roll}."
        )
        return BattleResult(challenger, None, log, challenger_roll, opponent_roll)

    log = (
        f"O autômato {bot.name} desestabiliza {challenger.name}, "
        f"obtendo {opponent_roll} contra {challenger_roll}."
    )
    return BattleResult(None, challenger, log, challenger_roll, opponent_roll)
