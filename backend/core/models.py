from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Maquina(models.Model):
    setor = models.CharField(max_length=100)
    cod_serie = models.IntegerField(unique=True)
    funcao = models.CharField(max_length = 100)
    marca = models.CharField(max_length = 100)
    nome = models.CharField(max_length = 100)
    apelido = models.CharField(max_length=100, blank=True, null=True)
    data_entrada = models.DateField()

    def __str__(self):
        return self.nome

class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    empresa = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.email
