# config.py

class Config:
    # Flask
    DEBUG = False
    SECRET_KEY = 'softwavesafllm'

    # MQTT


    MQTT_BROKER_URL  = '4618716853294e04861915e4d6cafb4a.s1.eu.hivemq.cloud'
    MQTT_BROKER_PORT = 8883
    MQTT_TOPICS = ['softwaves/dht11', 'softwaves/presenca']
    MQTT_TLS_ENABLED = True
    MQTT_USERNAME = "softwaves"
    MQTT_PASSWORD = "#Softwaves2024"



    # MySQL
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'softwavesafllm'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
