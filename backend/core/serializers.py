
#Esse é o arquivo que fazer a ponte entre banco e as requisições das informações
from rest_framework import serializers
from .models import Maquina,Usuario
from .models.sensor_data_store import DadosMaquina


#Classes para retornar as respostas de requisições

class MaquinaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Maquina
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = '__all__'

class DadosMaquinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DadosMaquina
        fields = '__all__'
