# Django
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages

# Project
from receitas.models import Receita

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if not nome.strip():
            messages.error(request, 'Campo nome obrigatório')
            return redirect('cadastro')

        if not email.strip():
            messages.error(request, 'Compo email obrigatório')
            return redirect('cadastro')

        if password != password2:
            messages.error(request, 'As senhas não são iguais')
            return redirect('cadastro')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email já existente')
            return redirect('cadastro')

        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Nome já existente')
            return redirect('cadastro')

        user = User.objects.create_user(username=nome, email=email, password=password)
        user.save()

        messages.success(request, 'Conta criada com sucesso')
        return redirect('login')

    return render(request, 'usuarios/cadastro.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if email == '' or password == '':
            messages.error(request, 'Campos obrigatórios')
            return redirect('login')

        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Erro ao tentar fazer o login, verifique suas credenciais e tente novamente')
                return redirect('login')

    return render(request, 'usuarios/login.html')

def cria_receita(request):
    if request.method == 'POST':
        nome_receita = request.POST.get('nome_receita')
        ingredientes = request.POST.get('ingredientes')
        modo_preparo = request.POST.get('modo_preparo')
        tempo_preparo = request.POST.get('tempo_preparo')
        rendimento = request.POST.get('rendimento')
        categoria = request.POST.get('categoria')
        foto_receita = request.FILES.get('foto_receita')
        get_publica = request.POST.get('publica')
        user = get_object_or_404(User, pk=request.user.pk)

        publica = False
        if get_publica == 'on':
            publica = True

        receita = Receita.objects.create(
            pessoa=user,
            nome_receita=nome_receita,
            ingredientes=ingredientes,
            modo_preparo=modo_preparo,
            tempo_preparo=tempo_preparo,
            redimento=rendimento,
            categoria=categoria,
            foto_receita=foto_receita,
            publica=publica
        )
        receita.save()
        messages.success(request, 'Receita criada com sucesso')
        return redirect('dashboard')
    else:
        return render(request, 'usuarios/cria_receita.html')

def dashboard(request):
    if request.user.is_authenticated:
        user_id = request.user.pk
        receitas = Receita.objects.filter(pessoa=user_id).order_by('-data_receita')

        return render(request, 'usuarios/dashboard.html', {'receitas': receitas})
    else:
        return redirect('index')

def logout(request):
    auth.logout(request)

    return redirect('index')
