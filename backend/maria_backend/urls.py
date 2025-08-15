from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from core.serializers import MyTokenObtainPairSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')), #nome do app
    # Gera os tokens JWT (crachás de autenticação) necessários para um login real
    # o token  vai serseja gerado com o campo 'is_staff'.
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]