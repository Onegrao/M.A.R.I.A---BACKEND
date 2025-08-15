from django.shortcuts import render
from rest_framework import viewsets
from .models import Maquina,Usuario, ConfiguracoesUsuario
from .serializers import MaquinaSerializer,UsuarioSerializer, PerfilUsuarioSerializer,ConfiguracoesUsuarioSerializer
from rest_framework.generics import RetrieveUpdateAPIView #serve p/ buscar (GET) e atualizar (PUT/PATCH) um único objeto
from rest_framework.permissions import IsAuthenticated, IsAdminUser #so admin pode ter acesso
# #restringir o acesso de uma view

# Create your views here.

class MaquinaViewSet(viewsets.ModelViewSet):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser] #view restrita so pra adm
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class PerfilAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PerfilUsuarioSerializer

    def get_object(self):
        # Retorna sempre o usuário que está fazendo a requisição
        return self.request.user

#VIEW PARA O USUÁRIO LOGADO VER/EDITAR SUAS PRÓPRIAS CONFIGURAÇÕES.
class ConfiguracoesAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConfiguracoesUsuarioSerializer

    def get_object(self):
        # Retorna as configurações associadas ao usuário da requisição
        return self.request.user.configuracoes

