# Django
from django.db import models
from datetime import datetime

# Local
from pessoas.models import Pessoas

class Receita(models.Model):
    foto_receita = models.ImageField(upload_to='fotos/%d/%m/%Y/', blank=True)
    nome_receita = models.CharField(max_length=200)
    ingredientes = models.TextField()
    modo_preparo = models.TextField()
    tempo_preparo = models.IntegerField()
    redimento = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    pessoa = models.ForeignKey(Pessoas, on_delete=models.CASCADE)
    publicada = models.BooleanField(default=False)
    data_receita = models.DateField(default=datetime.now, blank=True)
