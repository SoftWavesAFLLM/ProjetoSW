from flask import Flask
from flask_cors import CORS
from endpoint import api_bp
import gestor_mqtt as gestor_mqtt

# escolha o perfil que quiser:
from config import DevelopmentConfig  as ActiveConfig
# from config import ProductionConfig as ActiveConfig

def create_app():
    app = Flask(__name__)
    CORS(app)

    # carrega TODAS as configs (Flask, MQTT, MySQL...) de uma vez
    app.config.from_object(ActiveConfig)

    # inicializa o MQTT (ele vai ler broker, porta e tópicos de app.config)
    gestor_mqtt.init_mqtt(app)

    # registra o blueprint de rotas
    app.register_blueprint(api_bp)

    return app

if __name__ == '__main__':
    app = create_app()

    # loop MQTT em background
    gestor_mqtt.mqtt_client.loop_start()

    # sobe o servidor HTTP
    app.run(host='0.0.0.0', port=5000)
