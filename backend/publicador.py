import paho.mqtt.client as mqtt
import time
import random
import json  # Importa o módulo JSON

BROKER = "localhost"  # Use um broker público ou local
PORT = 1884
TOPIC = "topico/dados"

def simulate_data():
    # Simula dados de sensores
    return {
        "vibracao": str(round(random.uniform(05.0, 100.0), 2)) + ' microns',
        "consumo": str(round(random.uniform(6.0, 32.0), 2)) + ' Kw/h',
    }

# Configurando o cliente MQTT
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Conectado ao broker MQTT com código de retorno:", rc)

client.on_connect = on_connect

# Conectar ao broker
client.connect(BROKER, PORT, 60)
client.loop_start()

try:
    while True:
        # Simula dados
        dados = simulate_data()
        # Converte para JSON antes de enviar
        payload = json.dumps(dados)  
        client.publish(TOPIC, payload)  # Publica no tópico
        print(f"Publicado no tópico '{TOPIC}': {payload}")
        time.sleep(2)  # Intervalo entre mensagens
except KeyboardInterrupt:
    print("Encerrando...")
finally:
    client.loop_stop()
    client.disconnect()
