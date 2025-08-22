#Aqui é configurado quem vai puxar os dados recebidos e msotrar no front
# core/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class DadosMaquinaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("dados_maquina", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("dados_maquina", self.channel_name)

    async def send_dados(self, event):
        dados = event['dados']
        await self.send(text_data=json.dumps(dados))
