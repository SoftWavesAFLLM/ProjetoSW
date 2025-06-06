# config.py

class Config:
    # Flask
    DEBUG      = False
    SECRET_KEY = 'troque_esta_chave_por_uma_secreta'

    # MQTT
    MQTT_BROKER_URL  = '10.135.60.17'
    MQTT_BROKER_PORT = 1884
    MQTT_TOPICS      = [
        'topico/dados',
        # use 'sensores/#' para todos os sensores
    ]

    # MySQL
    MYSQL_HOST     = 'localhost'
    MYSQL_PORT     = 3306
    MYSQL_USER     = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB       = 'softwavesafllm'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
