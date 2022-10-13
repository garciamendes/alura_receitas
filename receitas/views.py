# Django
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Local
from .models import Receita


def index(request):
    if request.user.is_authenticated:
        receitas = Receita.objects.all().order_by('-data_receita')
        paginator = Paginator(receitas, 3)
        page = request.GET.get('page', 1)
        receita_por_pagina = paginator.get_page(page)
    else:
        receitas = Receita.objects.filter(publicada=True, publica=True).order_by('-data_receita')
        paginator = Paginator(receitas, 5)
        page = request.GET.get('page', 1)
        receita_por_pagina = paginator.get_page(page)

    return render(request, 'index.html', {'receitas': receita_por_pagina})


def receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)

    return render(request, 'receita.html', {'receita': receita})


def buscar(request):
    lista_receitas = Receita.objects.all().filter(publicada=True).order_by('-id')

    if 'search' in request.GET:
        nome_a_buscar = request.GET['search']
        lista_receitas = lista_receitas.filter(nome_receita__icontains=nome_a_buscar)

    dados = {
        'receitas': lista_receitas
    }

    return render(request, 'busca.html', dados)
