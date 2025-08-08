from django.shortcuts import render
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dados_protegidos(request):
    #Conteudo só pode ser visto por usuario autenticado
    content = {
        'message': f'Ola, {request.user.username}! Você está acessando uma área protegida.',
        'user_id': request.user.pk
    }
    return Response(content)

