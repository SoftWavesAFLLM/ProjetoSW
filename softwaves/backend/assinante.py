import paho.mqtt.client as mqtt

BROKER = "4618716853294e04861915e4d6cafb4a.s1.eu.hivemq.cloud"  # Mesmo broker usado pelo publicador
PORT = 8883
TOPIC_DHT11 = "softwaves/dht11"
TOPIC_PRESENCA = "softwaves/presenca"
USERNAME = "softwaves"
PASSWORD = "#Softwaves2024"

def on_connect(client, userdata, flags, rc, properties=None):
    app = userdata
    print(f"[MQTT] Conectado (rc={rc})")
    print("MQTT_TOPICS lidos do config:", app.config['MQTT_TOPICS'])
    for topic in app.config['MQTT_TOPICS']:
        client.subscribe(topic)
        print(f"[MQTT] Inscrito em {topic}")

def on_message(client, userdata, msg):
    print(f"Mensagem recebida no tópico '{msg.topic}': {msg.payload.decode()}")

# Configurando o cliente MQTT
client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

# Conectar ao broker
client.connect(BROKER, PORT, 60)
client.loop_forever()
