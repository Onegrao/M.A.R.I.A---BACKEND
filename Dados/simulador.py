import requests
import numpy as np
import time
import random
import json
from datetime import datetime


#BACKEND_URL = 'http://localhost:8000/api/sensores' #Endpoint do back para anlise de dados

NUM_MACHINES = 2 #ALTERAR ESSA INFORMAÇÃO DE ACORDO COM AS MAQUINAS INSERIDADS NO SISTEMA
SIMULATION_INTERVAL = 1 #Tempo de simulação


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



def generate_sensor_data(machine_id, last_data=None):
    config = MACHINE_CONFIG.get(machine_id)

    if last_data is None:
        last_data = {key: config[key]['base'] for key in config}
    
    current_time = datetime.now().strftime("%H:%M:%S %d%Y-%m")


    data = {
        'machine_id': machine_id,
        'timestamp': current_time,
    }

    for sensor, params in config.items():
        noise = np.random.normal(loc=0, scale=params['noise'])
        drift = params['drift']
        new_value = last_data.get(sensor, params['base'])

        data[sensor] = round(max(0, new_value), 2)

    return data

#def send_data_to_backend(data):

#    try :
        #response = requests.post(BACKEND_URL, json=data, timeout=5)
        #response.raise_for_status()
        #print(f"Dados enviados com sucesso: {data} -> Reposta do backend: {response.status_code}")
#        print(f"Dados enviados: {data}")
#    except requests.exceptions.RequestException as e:
#        print(f"Erro ao enviar dados: {e}")


if __name__ == "__main__":
    print(f"Iniciando a simulação para {NUM_MACHINES} máquinas...")

    # Armazena o último estado de cada máquina para simular a deriva
    current_state = {f'machine_{i+1}': None for i in range(NUM_MACHINES)} 

    try:
        while True:
            for machine_id in current_state.keys():

                sensor_data = generate_sensor_data(machine_id, current_state[machine_id])
                    

                current_state[machine_id] = {
                    key: sensor_data[key] for key in sensor_data if key not in ['machine_id', 'timestamp']
                }

                print(f"Dados gerados para {machine_id}: {json.dumps(sensor_data, indent=2)}")
            
            # Espera 1 segundo antes de enviar a próxima leva de dados
            print("-" * 50)
            time.sleep(15)
    except KeyboardInterrupt:
        print("\nSimulação encerrada pelo usuário.")
