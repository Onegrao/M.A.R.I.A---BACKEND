from django.shortcuts import render
from rest_framework import viewsets
from .models import Maquina,Usuario
from .serializers import MaquinaSerializer,UsuarioSerializer

# Create your views here.

class MaquinaViewSet(viewsets.ModelViewSet):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

