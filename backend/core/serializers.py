
#Esse é o arquivo que fazer a ponte entre banco e as requisições das informações
from rest_framework import serializers
from .models import Maquina,Usuario, ConfiguracoesUsuario


#Classes para retornar as respostas de requisições

class MaquinaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Maquina #adicionei status que estava faltando
        # Campos que o usuário pode ver das máquinas.
        fields = ['id', 'nome', 'apelido', 'status', 'setor', 'cod_serie', 'funcao', 'marca', 'data_entrada']

class UsuarioSerializer(serializers.ModelSerializer): #para admin poder acessar/alterar todos os usuários

    class Meta:
        model = Usuario
        fields = '__all__'

class PerfilUsuarioSerializer(serializers.ModelSerializer): #para o próprio usuário acessar/editar seu perfil.
    # O frontend usa 'nome', mas o Django usa 'first_name'. O 'source' faz a ponte.
    nome = serializers.CharField(source='first_name', required=False, allow_blank=True)
    class Meta:
        model = Usuario
        # Campos que o usuário pode ver e editar em seu perfil.
        fields = ['id', 'nome', 'email', 'cargo', 'empresa', 'telefone','cep', 'logradouro','numero', 'bairro', 'cidade', 'estado']
        read_only_fields = ['id', 'cargo']  # não deve ser alterado

class ConfiguracoesUsuarioSerializer(serializers.ModelSerializer):
    notificacoesPorEmail = serializers.BooleanField(source='notificacoes_por_email')
    class Meta:
        model = ConfiguracoesUsuario
        fields = ['notificacoesPorEmail', 'tema']