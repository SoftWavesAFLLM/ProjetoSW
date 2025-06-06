import paho.mqtt.client as mqtt

BROKER = "10.135.60.17"  # Mesmo broker usado pelo publicador
PORT = 1884
TOPIC = "topico/dados"

def on_connect(client, userdata, flags, rc):
    print("Conectado ao broker MQTT com código de retorno:", rc)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    print(f"Mensagem recebida no tópico '{msg.topic}': {msg.payload.decode()}")

# Configurando o cliente MQTT
client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

# Conectar ao broker
client.connect(BROKER, PORT, 60)
client.loop_forever()
