# django
from django.contrib import admin

# Local
from .models import Pessoas

class ListaPessoas(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email')
    list_display_links = ('id', 'nome')
    search_fields = ('nome',)
    list_per_page = 5

admin.site.register(Pessoas, ListaPessoas)
