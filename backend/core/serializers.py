
#Esse é o arquivo que fazer a ponte entre banco e as requisições das informações
from rest_framework import serializers
from .models import Maquina,Usuario, ConfiguracoesUsuario
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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

def create(self, validated_data):
    #Esta função garante que a senha seja salva corretamente
    #para que o novo usuário consiga fazer login. Se nao tiver ela
    #o novo usuario nao consegue pq a auten. nao funciona cm texto puro
    # Cria um usuário usando o método padrão do Django, que lida com a senha
    user = Usuario.objects.create_user(**validated_data)
    return user

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

# O objetivo da classe é "turbinar" o token JWT padrão pq por padrão, o token só vem com o ID do usuário
# mas precisa saber se o usuário é um admin (is_staff) lá no meu front .
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # ai o metodo ja me da o token básico pronto.
        token = super().get_token(user)
        token['is_staff'] = user.is_staff
        return token