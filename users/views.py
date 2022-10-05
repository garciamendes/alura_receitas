# Django
from genericpath import exists
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth


def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if not nome.strip():
            return redirect('cadastro')

        if not email.strip():
            return redirect('cadastro')

        if password != password2:
            return redirect('cadastro')

        if User.objects.filter(email=email).exists():
            return redirect('cadastro')

        user = User.objects.create_user(username=nome, email=email, password=password)
        user.save()

        return redirect('login')

    return render(request, 'usuarios/cadastro.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if email == '' or password == '':
            return redirect('login')

        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')

    return render(request, 'usuarios/login.html')

def dashboard(request):
    return render(request, 'usuarios/dashboard.html')

def logout(request):
    auth.logout(request)

    return redirect('index')
