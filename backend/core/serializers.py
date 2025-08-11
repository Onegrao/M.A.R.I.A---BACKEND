
#Esse é o arquivo que fazer a ponte entre banco e as requisições das informações
from rest_framework import serializers
from .models import Maquina,Usuario


#Classes para retornar as respostas de requisições

class MaquinaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Maquina #adicionei status que estava faltando
        fields = ['id', 'nome', 'apelido', 'status', 'setor', 'cod_serie', 'funcao', 'marca', 'data_entrada']

class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = '__all__'
