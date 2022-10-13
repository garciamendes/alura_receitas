# Django
from django.shortcuts import get_object_or_404, render

# Local
from .models import Receita


def index(request):
    if request.user.is_authenticated:
        receitas = Receita.objects.all().order_by('-data_receita')
    else:
        receitas = Receita.objects.filter(publicada=True, publica=True).order_by('-data_receita')

    return render(request, 'index.html', {'receitas': receitas})


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
