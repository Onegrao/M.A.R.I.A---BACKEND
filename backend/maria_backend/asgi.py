# myproject/asgi.py (SOLUÇÃO CONSOLIDADA)

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import re_path

# 1. IMPORTA O CONSUMER DIRETAMENTE (sem usar o core.routing)
from core import consumers 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maria_backend.settings')

# 2. DEFINE A LISTA DE URLS AQUI
websocket_urlpatterns = [
    re_path(r'ws/data/$', consumers.DataConsumer.as_asgi()), 
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(websocket_urlpatterns),
})