import paho.mqtt.client as paho
from paho import mqtt
import time
import random
import json  # Importa o módulo JSON

# Configurações do HiveMQ Cloud
BROKER = "4618716853294e04861915e4d6cafb4a.s1.eu.hivemq.cloud"
PORT = 8883
TOPIC = "sensores/#"
USERNAME = "softwaves"
PASSWORD = "#Softwaves2024"

def simulate_data():
    # Simula dados de sensores
    return {
        "vibracao": f"{round(random.uniform(5.0, 100.0), 2)} microns",
        "consumo": f"{round(random.uniform(6.0, 32.0), 2)} Kw/h",
    }

# Criando cliente MQTT v5
client = paho.Client(protocol=paho.MQTTv5)

# Habilitar TLS
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

# Definir credenciais
client.username_pw_set(USERNAME, PASSWORD)

def on_connect(client, userdata, flags, rc, properties=None):
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