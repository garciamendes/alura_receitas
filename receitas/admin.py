from django.contrib import admin

from receitas.models import Receita

class ListaReceita(admin.ModelAdmin):
    list_display = ('id', 'nome_receita')
    list_display_links = ('id', 'nome_receita')

admin.site.register(Receita, ListaReceita)
