

import json
import time
# Usamos AsyncWebsocketConsumer para permitir que o Django faça outras coisas enquanto espera
from channels.generic.websocket import AsyncWebsocketConsumer 

class DataConsumer(AsyncWebsocketConsumer):
    # 1. Conexão Aceita
    async def connect(self):
        await self.accept()
        print("Novo cliente Angular conectado.")
        
        # 1.1. Envia uma mensagem inicial de status
        await self.send(text_data=json.dumps({
            "type": "connection.status",
            "message": "Conectado ao servidor Django Channels."
        }))

        # 1.2. Inicia o envio de dados de teste de forma assíncrona
        # (Em produção, isso seria um loop de 'while True' ou um scheduler de tarefas)
        await self.send_test_data() 

    # 2. Receber dados do cliente (Ex: quando o Angular envia um 'ping')
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(f"Mensagem recebida do Angular: {text_data_json}")

        # Envia uma resposta (echo) de volta ao Angular
        await self.send(text_data=json.dumps({
            "type": "echo.message",
            "message": f"Servidor recebeu o ping às {time.strftime('%H:%M:%S')}"
        }))

    # 3. Envio de dados (simulador de stream)
    async def send_test_data(self):
        # Exemplo: envia 5 mensagens para o cliente
        for i in range(1, 6):
            data = {
                "type": "data.update",
                "message": {
                    "sensor_id": 42,
                    "value": f"Stream de Valor {i}",
                    "timestamp": time.time()
                }
            }
            await self.send(text_data=json.dumps(data))
            # O 'time.sleep' não funciona em async. Em async, usamos 'await asyncio.sleep(3)'
            # Para este teste simples, se você rodar com Daphne, ele vai funcionar
            time.sleep(3) 

    # 4. Desconexão
    async def disconnect(self, close_code):
        print(f"Cliente desconectado (código: {close_code})")