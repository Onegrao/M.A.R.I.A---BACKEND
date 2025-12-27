# mqtt_listener.py

import paho.mqtt.client as mqtt
import json
import time
import os
import django
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import sys


sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # adiciona o diretório atual ao PYTHONPATH
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.maria_backend.settings')


# --- Configurações ---
BROKER_ADDRESS = "localhost" 
BROKER_PORT = 1883
TOPIC = "maquina/dados/#"
CHANNEL_GROUP_NAME = 'realtime_machine_data' # DEVE CORRESPONDER ao Consumer

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Conectado ao broker MQTT com código: {reason_code}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    try:
        payload_str = msg.payload.decode()
        data = json.loads(payload_str)
        
        # 1. Obtém o Channel Layer
        channel_layer = get_channel_layer()

        # 2. Envia a mensagem para o grupo de WebSockets
        # O 'type': 'data.update' é o que dispara o método data_update no Consumer
        async_to_sync(channel_layer.group_send)(
            CHANNEL_GROUP_NAME,
            {
                'type': 'data.update',  
                'text': json.dumps(data) # Envie a mensagem como string JSON
            }
        )

        print(f"MQTT para Channel Layer: {data}")

    except json.JSONDecodeError:
        print(f"Erro ao decodificar o JSON: {msg.payload}")
    except Exception as e:
        print(f"Erro ao enviar para o Channel Layer: {e}")

def main():
    client = mqtt.Client(protocol=mqtt.MQTTv5, transport="tcp", userdata=None, 
                         callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    
    while True:
        try:
            client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
            break
        except Exception as e:
            time.sleep(5)
            
    client.loop_forever()

if __name__ == "__main__":
    main()