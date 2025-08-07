from django.shortcuts import render
from .models import Maquina,Usuario
from .serializers import MaquinaSerializer,UsuarioSerializer

# Create your views here.

class MaquinaViewSet(viewsets.ModelViewSet):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer

class UsuarioViewSet(viewsets.ModelViewset):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

