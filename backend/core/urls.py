#Rotas que irao receber e encaminhar as requisições vindas do front

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MaquinaViewSet,UsuarioViewSet

#cria todas as rotas padrão
router = DefaultRouter() #Nao sei pq isso aqui precisar existir kkk
router.register(r'maquinas', MaquinaViewSet, basename='maquina')
router.register(r'Usuarios',UsuarioViewSet)

urlpatterns = [
    path('',include(router.urls)),
]