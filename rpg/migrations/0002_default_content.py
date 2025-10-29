# Default playable content for the RPG module.

# Django
from django.db import migrations


def create_content(apps, schema_editor):
    Mission = apps.get_model('rpg', 'Mission')
    TrainingBot = apps.get_model('rpg', 'TrainingBot')

    missions = [
        {
            'name': 'Resgatar o Mensageiro',
            'description': 'Um emissário foi capturado por bandidos. Localize o esconderijo e traga-o com vida.',
            'difficulty': 'standard',
            'minimum_level': 1,
            'success_rate': 75,
            'experience_reward': 80,
            'gold_reward': 60,
        },
        {
            'name': 'Sombras em Ilyndor',
            'description': 'Criaturas etéreas rondam as catacumbas da cidade. Precisa-se de coragem para selar o portal.',
            'difficulty': 'heroic',
            'minimum_level': 3,
            'success_rate': 65,
            'experience_reward': 140,
            'gold_reward': 120,
        },
        {
            'name': 'O Tesouro Afundado',
            'description': 'Uma embarcação antiga reapareceu na costa. Explore-a e recupere artefatos antes que afunde novamente.',
            'difficulty': 'legendary',
            'minimum_level': 5,
            'success_rate': 50,
            'experience_reward': 220,
            'gold_reward': 250,
        },
    ]

    for mission in missions:
        Mission.objects.get_or_create(name=mission['name'], defaults=mission)

    bots = [
        {
            'name': 'Maniquim de Madeira',
            'description': 'Ideal para aprender os fundamentos de combate.',
            'power_rating': 4,
            'experience_reward': 30,
            'gold_reward': 15,
        },
        {
            'name': 'Guardião Arcano',
            'description': 'Projeta barreiras mágicas e dispara rajadas de energia.',
            'power_rating': 9,
            'experience_reward': 70,
            'gold_reward': 40,
        },
        {
            'name': 'Colosso Mecânico',
            'description': 'Uma máquina pesada focada em resistência e força bruta.',
            'power_rating': 14,
            'experience_reward': 120,
            'gold_reward': 80,
        },
    ]

    for bot in bots:
        TrainingBot.objects.get_or_create(name=bot['name'], defaults=bot)


def remove_content(apps, schema_editor):
    Mission = apps.get_model('rpg', 'Mission')
    TrainingBot = apps.get_model('rpg', 'TrainingBot')

    mission_names = [
        'Resgatar o Mensageiro',
        'Sombras em Ilyndor',
        'O Tesouro Afundado',
    ]
    bot_names = [
        'Maniquim de Madeira',
        'Guardião Arcano',
        'Colosso Mecânico',
    ]

    Mission.objects.filter(name__in=mission_names).delete()
    TrainingBot.objects.filter(name__in=bot_names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('rpg', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_content, remove_content),
    ]
