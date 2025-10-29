# Generated manually to introduce the RPG game models.

# Django
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Nome')),
                ('concept', models.CharField(help_text='Resumo rápido do personagem.', max_length=120, verbose_name='Conceito')),
                ('origin', models.CharField(blank=True, help_text='Cidade, clã ou organização.', max_length=120, verbose_name='Origem')),
                ('archetype', models.CharField(help_text='Classe ou função dentro do grupo.', max_length=80, verbose_name='Arquétipo')),
                ('strength', models.PositiveIntegerField(default=1, verbose_name='Força')),
                ('agility', models.PositiveIntegerField(default=1, verbose_name='Agilidade')),
                ('intellect', models.PositiveIntegerField(default=1, verbose_name='Intelecto')),
                ('spirit', models.PositiveIntegerField(default=1, verbose_name='Espírito')),
                ('vitality', models.PositiveIntegerField(default=1, verbose_name='Vitalidade')),
                ('experience', models.PositiveIntegerField(default=0, verbose_name='Experiência')),
                ('gold', models.PositiveIntegerField(default=0, verbose_name='Ouro')),
                ('level', models.PositiveIntegerField(default=1, verbose_name='Nível')),
                ('hit_points', models.PositiveIntegerField(default=10, verbose_name='Pontos de Vida')),
                ('mana', models.PositiveIntegerField(default=5, verbose_name='Mana')),
                ('biography', models.TextField(blank=True, help_text='Um pouco sobre as motivações do herói.', verbose_name='História')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(blank=True, help_text='Usuário responsável pela ficha, quando autenticado.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rpg_characters', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Personagem',
                'verbose_name_plural': 'Personagens',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, verbose_name='Nome')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('difficulty', models.CharField(choices=[('easy', 'Fácil'), ('standard', 'Normal'), ('heroic', 'Heróica'), ('legendary', 'Lendária')], default='standard', max_length=12, verbose_name='Dificuldade')),
                ('minimum_level', models.PositiveIntegerField(default=1, verbose_name='Nível mínimo')),
                ('success_rate', models.PositiveIntegerField(default=70, help_text='Probabilidade base antes de bônus.', verbose_name='Chance de sucesso (%)')),
                ('experience_reward', models.PositiveIntegerField(default=50, verbose_name='Experiência')),
                ('gold_reward', models.PositiveIntegerField(default=30, verbose_name='Ouro')),
            ],
            options={
                'verbose_name': 'Missão',
                'verbose_name_plural': 'Missões',
                'ordering': ['minimum_level', 'name'],
            },
        ),
        migrations.CreateModel(
            name='TrainingBot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Nome')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('power_rating', models.PositiveIntegerField(default=5, verbose_name='Nível de poder')),
                ('experience_reward', models.PositiveIntegerField(default=20, verbose_name='Experiência')),
                ('gold_reward', models.PositiveIntegerField(default=10, verbose_name='Ouro')),
            ],
            options={
                'verbose_name': 'Autômato de treino',
                'verbose_name_plural': 'Autômatos de treino',
                'ordering': ['power_rating'],
            },
        ),
        migrations.CreateModel(
            name='Battle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log', models.TextField(verbose_name='Relato da batalha')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_training', models.BooleanField(default=False, verbose_name='Treino')),
                ('bot', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='battles', to='rpg.trainingbot')),
                ('challenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='battles_as_challenger', to='rpg.character')),
                ('opponent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='battles_as_opponent', to='rpg.character')),
                ('winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='battles_won', to='rpg.character')),
            ],
            options={
                'verbose_name': 'Batalha',
                'verbose_name_plural': 'Batalhas',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='MissionAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('success', models.BooleanField(default=False, verbose_name='Sucesso')),
                ('summary', models.TextField(verbose_name='Resumo')),
                ('experience_earned', models.PositiveIntegerField(default=0, verbose_name='Experiência recebida')),
                ('gold_earned', models.PositiveIntegerField(default=0, verbose_name='Ouro recebido')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mission_attempts', to='rpg.character')),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='rpg.mission')),
            ],
            options={
                'verbose_name': 'Conclusão de missão',
                'verbose_name_plural': 'Conclusões de missão',
                'ordering': ['-created_at'],
            },
        ),
    ]
