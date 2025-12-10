from flask import Flask
from flask_cors import CORS
from endpoint import api_bp
import gestor_mqtt as gestor_mqtt


from config import DevelopmentConfig as ActiveConfig

def create_app():
    app = Flask(__name__)
    CORS(app)


    # Carrega configs antes de inicializar MQTT
    app.config.from_object(ActiveConfig)

    # Inicializa MQTT com Flask appA
    gestor_mqtt.init_mqtt(app)

    # Registra blueprint de rotas
    app.register_blueprint(api_bp)

    return app

if __name__ == '__main__':
    app = create_app()

    # NÃO precisa rodar loop_start() de novo, já está no init_mqtt
    # gestor_mqtt.mqtt_client.loop_start()

    # Sobe servidor Flask
    app.run(host='0.0.0.0', port=5000, use_reloader=False)
