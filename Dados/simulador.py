#import requests
import numpy as np
import time
import random
import json
import paho.mqtt.client as mqtt
from datetime import datetime

BROKER_ADDRESS = "localhost" #IP do broker
BROKER_PORT = 1883
TOPIC = "maquina/dados" #Mesmo topico para onde o simulador envia


NUM_MACHINES = 2 #ALTERAR ESSA INFORMAÇÃO DE ACORDO COM AS MAQUINAS INSERIDADS NO SISTEMA
SIMULATION_INTERVAL = 5 #Tempo de simulação


MACHINE_CONFIG = { #Parametros normais das maquinas
    'machine_1': {
        'temperature': {'base': 75.0, 'noise': 1.5, 'drift': 0.05}, # Valor padrão (base), ruido (noise), deriva (drift)
        'voltage': {'base': 380.0, 'noise': 2.0, 'drift': 0.1},
        'amperage': {'base': 15.0, 'noise': 0.5, 'drift': 0.02},
        'pressure': {'base': 5.0, 'noise': 0.2, 'drift': 0.01},
        'rpm': {'base': 5000.0, 'noise': 50.0, 'drift': 1.0}
    },
    'machine_2': {
        'temperature': {'base': 68.0, 'noise': 1.0, 'drift': -0.03},
        'voltage': {'base': 378.0, 'noise': 1.5, 'drift': 0.08},
        'amperage': {'base': 12.0, 'noise': 0.3, 'drift': -0.01},
        'pressure': {'base': 4.5, 'noise': 0.1, 'drift': 0.005},
        'rpm': {'base': 4800.0, 'noise': 40.0, 'drift': 0.8}
    }
}

machine_states = {f'machine_{i+1}': None for i in range(NUM_MACHINES)} #Armazena o ultimo estado de cada maquina


def generate_sensor_data(machine_id, last_data=None):
    config = MACHINE_CONFIG.get(machine_id)
    last_data = machine_states[machine_id]

    if last_data is None:
        last_data = {key: config[key]['base'] for key in config}
    current_time = datetime.now().strftime("%H:%M:%S %d%Y-%m")

    data = {
        'machine_id': machine_id,
        'timestamp': current_time,
    }

    new_state = {}
    for sensor, params in config.items():
        noise = np.random.normal(loc=0, scale=params['noise'])
        drift = params['drift']
        new_value = last_data[sensor] + noise + params['drift']

        new_state[sensor] = new_value
        data[sensor] = round(max(0, new_value), 2)

    machine_states[machine_id] = new_state
    return data

#Logica de publish no broker MQTT
def publish_data_to_mqtt(client, topic, data):
    try:
        json_payload = json.dumps(data)
        client.publish(topic, json_payload)
        print(f"Dados publicados no tópico {topic}: {json_payload}")
    except Exception as e:
        print(f"Erro ao publicar dados no MQTT: {e}")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao broker MQTT com sucesso.")
    else:
        print(f"Falha ao conectar ao broker MQTT, código de retorno: {rc}")



if __name__ == "__main__":
    print(f"Iniciando a simulação para {NUM_MACHINES} máquinas...")

    client = mqtt.Client(protocol=mqtt.MQTTv5)
    client.on_connect = on_connect

    try:
        client.connect(BROKER_ADDRESS, BROKER_PORT,60)
        client.loop_start()
    except Exception as e:
        print(f"Erro ao conectar ao broker MQTT: {e}")
        exit()
    
    try:
        while True:
            for machine_id in machine_states.keys():
                sensor_data = generate_sensor_data(machine_id)

                #Monta o tópico especifico para cada máquina
                topic = f"{TOPIC}/{machine_id}"

                #Publica os dados no broker MQTT
                publish_data_to_mqtt(client, topic, sensor_data)

                print("-" * 50)
                time.sleep(SIMULATION_INTERVAL)  # Espera o intervalo de simulação antes de gerar novos dados
    except KeyboardInterrupt:
        print("Simulação interrompida pelo usuário.")
    finally:
        client.loop_stop()
        client.disconnect()
        print("Desconectado do broker MQTT.")