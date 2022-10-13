# Django
from django.contrib import admin

# Local
from .models import Receita

class ListaReceita(admin.ModelAdmin):
    list_display = ('id', 'nome_receita', 'publicada', 'publica')
    list_display_links = ('id', 'nome_receita')
    search_fields = ('nome_receita',)
    list_filter = ('categoria',)
    list_per_page = 5

admin.site.register(Receita, ListaReceita)
