"""Forms used for managing RPG interactions."""

# Django
from django import forms

# Local
from .models import Character, Mission, TrainingBot


class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = [
            'name',
            'concept',
            'origin',
            'archetype',
            'strength',
            'agility',
            'intellect',
            'spirit',
            'vitality',
            'hit_points',
            'mana',
            'biography',
        ]
        widgets = {
            'biography': forms.Textarea(attrs={'rows': 4}),
        }


class DuelForm(forms.Form):
    challenger = forms.ModelChoiceField(
        queryset=Character.objects.all(),
        label='Seu personagem',
        help_text='Escolha o herói que desafiará o adversário.',
    )
    opponent = forms.ModelChoiceField(
        queryset=Character.objects.all(),
        label='Oponente',
        help_text='Selecione contra quem batalhar.',
    )

    def clean(self):
        cleaned_data = super().clean()
        challenger = cleaned_data.get('challenger')
        opponent = cleaned_data.get('opponent')
        if challenger and opponent and challenger == opponent:
            raise forms.ValidationError('Escolha personagens diferentes para o duelo.')
        return cleaned_data


class MissionAttemptForm(forms.Form):
    character = forms.ModelChoiceField(
        queryset=Character.objects.all(),
        label='Personagem',
    )

    def __init__(self, mission: Mission, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mission = mission
        self.fields['character'].queryset = Character.objects.filter(level__gte=mission.minimum_level)
        self.fields['character'].help_text = (
            f"Disponível para aventureiros a partir do nível {mission.minimum_level}."
        )


class TrainingBattleForm(forms.Form):
    character = forms.ModelChoiceField(
        queryset=Character.objects.all(),
        label='Personagem',
    )
    bot = forms.ModelChoiceField(queryset=TrainingBot.objects.all(), label='Autômato')

    def clean(self):
        cleaned_data = super().clean()
        character = cleaned_data.get('character')
        bot = cleaned_data.get('bot')
        if character and bot and character.level * 10 < bot.power_rating * 5:
            raise forms.ValidationError(
                'Este desafio é muito difícil! Evolua mais um pouco antes de enfrentar este autômato.'
            )
        return cleaned_data
