#Script que ira se conectar com o servico mqtt que roda no docker
import paho.mqtt.client as mqtt
import requests
import json
import time

# Configurações do Broker MQTT
BROKER_ADDRESS = "localhost" #IP do broker
BROKER_PORT = 1883
TOPIC = "maquina/dados" #Mesmo topico para onde o simulador envia os dados

DJANGO_API_URL = "http://localhost:8000/api/dados/" #rota Url onde vou receber os dados

def on_connet(client, userdata, flags, rc):
    print(f"Conectado ao broker MQTT com código: {rc}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    try:
        payload_str = msg.payload.decode()
        data = json.loads(payload_str)
        print(f"Dados recebidos do MQTT: {data}")

        #Envia os dados para a API Django
        response = requests.post(DJANGO_API_URL, json=data)

        if response.status_code == 201: #Dados criados
            print("Dados enviados ao Django com sucesso")
        else:
            print(f"Falha ao enviar os dados para o Django, erro: {response.status_code}" )
    
    except json.JSONDecodeError:
        print(f"Erro ao decodificar O JSON: {msg.payload}")
    except requests.exceptions.RequestsException as e:
        print(f"Erro ao enviar requisição HTTP para o Django: {e}")

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1) #VERSION1 serve para compatibilidade
    client.on_connect = on_connet
    client.on_message = on_message

    #Tenta reconectar a cada 5 segundos
    while True:
        try:
            client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
            break
        except Exception as e:
            print(f"Falha ao conectar ao broker MQTT: {e}. Tentando novamente em 5 segundos...")
            time.sleep(5)
    client.loop_forever()

if __name__ == "__main__":
    main()