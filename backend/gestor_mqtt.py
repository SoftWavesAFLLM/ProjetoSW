import paho.mqtt.client as mqtt

from psensor import inserir_sensor

mqtt_client = mqtt.Client()

def init_mqtt(app):
    # guarda a instância Flask no userdata para callbacks
    mqtt_client.user_data_set(app)
    mqtt_client.on_connect = _on_connect
    mqtt_client.on_message = _on_message

    # lê broker e porta direto do app.config
    broker = app.config['MQTT_BROKER_URL']
    port   = app.config['MQTT_BROKER_PORT']
    mqtt_client.connect(broker, port, keepalive=60)
    print(f"[MQTT] Conectando em {broker}:{port}...")

def _on_connect(client, userdata, flags, rc):
    app = userdata
    print(f"[MQTT] Conectado (rc={rc})")
    # lê lista de tópicos de app.config e faz subscribe
    for topic in app.config['MQTT_TOPICS']:
        client.subscribe(topic)
        print(f"[MQTT] Inscrito em {topic}")


def _on_message(client, userdata, msg):
    payload = msg.payload.decode()
    topico = msg.topic
    print(f"[MQTT] Mensagem → {topico}: {payload}")

    # grava no banco usando o CRUD de sensor
    resultado = inserir_sensor(topico, payload)
    print(f"[BD] {resultado}")