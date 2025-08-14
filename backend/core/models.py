from django.db import models
from django.contrib.auth.models import AbstractUser
# Imports para criar configurações automaticamente para novos usuários
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Maquina(models.Model):
    STATUS_CHOICES = [
        ('corretiva', 'Corretiva'),
        ('preventiva', 'Realizar Preventiva'),
        ('desligada', 'Desligada'),
    ]
    setor = models.CharField(max_length=100)
    cod_serie = models.IntegerField(unique=True)
    funcao = models.CharField(max_length = 100)
    marca = models.CharField(max_length = 100)
    nome = models.CharField(max_length = 100)
    apelido = models.CharField(max_length=100, blank=True, null=True)
    data_entrada = models.DateField()

    # Linha adicionada
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='desligada')
    def __str__(self):
        return self.nome

class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    empresa = models.CharField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    cep = models.CharField(max_length=10, blank=True, null=True)
    logradouro = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=20, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.email

#model para as configurações do usuário
class ConfiguracoesUsuario(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='configuracoes')
    notificacoes_por_email = models.BooleanField(default=True)
    tema = models.CharField(max_length=20, default='Tema Claro')

    def __str__(self):
        return f"Configurações de {self.usuario.username}"

# FUNÇÃO PARA CRIAR CONFIGS AUTOMATICAMENTE QUANDO UM USUÁRIO É CRIADO
# O RECEIVER automatiza a criação de configurações padrão smp que um novo usuário
# for inserido no banco
@receiver(post_save, sender=Usuario)
def criar_configuracoes_usuario(sender, instance, created, **kwargs):
    if created:
        ConfiguracoesUsuario.objects.create(usuario=instance)
