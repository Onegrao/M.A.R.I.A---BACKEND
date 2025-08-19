#Rotas que irao receber e encaminhar as requisições vindas do front

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MaquinaViewSet,UsuarioViewSet, login_check , DadosMaquinaCreateView
#dados_protegidos,login_check

router = DefaultRouter() #Nao sei pq isso aqui precisar existir kkk
router.register(r'Maquinas',MaquinaViewSet)
router.register(r'Usuarios',UsuarioViewSet)

urlpatterns = [
    path('',include(router.urls)),
   # path('dados-protegidos/', dados_protegidos, name='dados_protegidos'),
    path('login/', login_check, name='core.login')
    path('dados/', DadosMaquinaCreateView.as_view(), name='dados-api')
]