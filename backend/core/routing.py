# core/routing.py

from django.urls import re_path

from . import consumers # Assumindo que seu consumidor está em core/consumers.py

websocket_urlpatterns = [
    # Esta rota precisa CASAR EXATAMENTE com a URL no seu Angular!
    re_path(r'ws/data/$', consumers.DataConsumer.as_asgi()), 
]