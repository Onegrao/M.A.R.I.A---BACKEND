from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from .models import Maquina,Usuario
from .serializers import MaquinaSerializer,UsuarioSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Create your views here.

class MaquinaViewSet(viewsets.ModelViewSet):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    
#Parte para cuidar da autenticação

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def dados_protegidos(request):
#     #Conteudo só pode ser visto por usuario autenticado
#     content = {
#         'message': f'Ola, {request.user.username}! Você está acessando uma área protegida.',
#         'user_id': request.user.pk
#     }
#     return Response(content)

@api_view(['POST'])
def login_check(request):
    #Autentica o usuario a partir do username e senha
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        return Response({
            'message': 'Login bem-sucedido.'
            
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'error': 'Credenciais inválidas.'
        }, status = status.HTTP_400_BAD_REQUEST)
