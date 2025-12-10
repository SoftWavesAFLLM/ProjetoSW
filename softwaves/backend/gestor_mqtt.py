import paho.mqtt.client as paho
from paho import mqtt
from psensor import inserir_sensor
import json

mqtt_client = paho.Client(protocol=paho.MQTTv5)
socketio_instance = None

def init_mqtt(app, socketio=None):
    print("MQTT Topics carregados do config:", app.config.get('MQTT_TOPICS', []))

    global socketio_instance
    socketio_instance = socketio

    # Guarda tópicos localmente
    mqtt_client.topics = app.config.get('MQTT_TOPICS', [])

    # Configura callbacks
    mqtt_client.user_data_set(app)
    mqtt_client.on_connect = _on_connect
    mqtt_client.on_message = _on_message

    broker = app.config['MQTT_BROKER_URL']
    port = app.config['MQTT_BROKER_PORT']

    if app.config.get('MQTT_TLS_ENABLED', False):
        mqtt_client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

    if app.config.get('MQTT_USERNAME') and app.config.get('MQTT_PASSWORD'):
        mqtt_client.username_pw_set(app.config['MQTT_USERNAME'], app.config['MQTT_PASSWORD'])

    print(f"[MQTT] Conectando em {broker}:{port}...")
    mqtt_client.connect(broker, port, keepalive=60)
    mqtt_client.loop_start()


def _on_connect(client, userdata, flags, rc, properties=None):
    print("Inscrevendo tópicos:", getattr(client, "topics", []))

    print(f"[MQTT] Conectado (rc={rc})")
    print("Tópicos para inscrição:", getattr(client, "topics", []))
    for topic in getattr(client, "topics", []):
        client.subscribe(topic)
        print(f"[MQTT] Inscrito em {topic}")


def _on_message(client, userdata, msg):
    print(f"[DEBUG] Mensagem recebida em {msg.topic}: {msg.payload.decode()}")
    app = userdata
    with app.app_context():
        payload = msg.payload.decode()
        topico = msg.topic
        print(f"[MQTT] Mensagem recebida ? {topico}: {payload}")

        resultado = inserir_sensor(topico, payload)
        print(f"[BD] {resultado}")

        # Emit via SocketIO
        if socketio_instance:
            try:
                nome_sensor = topico.split('/')[-1]
                dados_para_emitir = {
                    'nome_sensor': nome_sensor,
                    'payload': json.loads(payload) if payload.startswith('{') else payload
                }
                socketio_instance.emit('novo_dado_sensor', dados_para_emitir)
                print(f"[WebSocket] Dados emitidos: {dados_para_emitir}")
            except Exception as e:
                print(f"[WebSocket] Erro ao emitir dados: {e}")
