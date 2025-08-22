from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from .models import Maquina, Usuario
from .serializers import MaquinaSerializer, UsuarioSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

# WebSocket (Channels) imports
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# ----------------- ViewSets -----------------
class MaquinaViewSet(viewsets.ModelViewSet):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

# ----------------- Receber dados do simulador -----------------
@api_view(['POST'])
def dados_realtime(request):
    dados = request.data
    print(f"Dados recebidos para análise: {dados}")

    # Aqui enviamos para o front via WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "dados_maquina",  # nome do grupo do WebSocket
        {
            "type": "send_dados",
            "dados": dados
        }
    )

    return Response({"message": "Dados recebidos e enviados para o front"}, status=status.HTTP_200_OK)

# ----------------- Autenticação -----------------
@api_view(['POST'])
def login_check(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    
    if user:
        return Response({"message": "Login bem-sucedido."}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Credenciais inválidas."}, status=status.HTTP_400_BAD_REQUEST)
