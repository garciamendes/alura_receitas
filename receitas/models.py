# Python
from datetime import datetime

# Django
from django.db import models
from django.contrib.auth.models import User

class Receita(models.Model):
    foto_receita = models.ImageField(upload_to='fotos/%d/%m/%Y/', blank=True)
    nome_receita = models.CharField(max_length=200)
    ingredientes = models.TextField()
    modo_preparo = models.TextField()
    tempo_preparo = models.IntegerField()
    redimento = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    pessoa = models.ForeignKey(User, on_delete=models.CASCADE)
    publicada = models.BooleanField(default=False)
    publica = models.BooleanField(default=False)
    data_receita = models.DateField(default=datetime.now, blank=True)
