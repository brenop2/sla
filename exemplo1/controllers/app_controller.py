# controllers/app_controller.py
# Diretório: EXEMPLO2/controllers/

from flask import Flask, render_template, request
from models.db import db, instance
from models.iot.read import Read 

# Blueprints
from controllers.sensors_controller import sensor_ 
from controllers.actuators_controller import actuator_
from controllers.reads_controller import read_
from controllers.users_controller import user_ 

# MQTT
import json 
from flask_mqtt import Mqtt # Instalar: pip install flask-mqtt

# Variáveis globais para MQTT
mqtt_client = Mqtt()
topic_subscribe = "/aula_flask/"

def create_app():
    app = Flask(__name__,
                template_folder="./views/",
                static_folder="./static/",
                root_path="./")

    # Configurações Flask-SQLAlchemy
    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key' 
    app.config['SQLALCHEMY_DATABASE_URI'] = instance
    db.init_app(app)
    
    # Configurações Flask-MQTT
    app.config['MQTT_BROKER_URL'] = 'mqtt-dashboard.com'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = '' 
    app.config['MQTT_PASSWORD'] = ''
    app.config['MQTT_KEEPALIVE'] = 5000
    app.config['MQTT_TLS_ENABLED'] = False
    
    # Inicializa o cliente MQTT
    mqtt_client.init_app(app) 
    
    # Registro dos Blueprints
    app.register_blueprint(sensor_, url_prefix='/')
    app.register_blueprint(actuator_, url_prefix='/')
    app.register_blueprint(read_, url_prefix='/') 
    app.register_blueprint(user_, url_prefix='/')
    
    @app.route('/')
    def index():
        return render_template("home.html")

    return app

# ====================================================================
# Funções de Callback do MQTT (fora da create_app, mas no mesmo arquivo)
# ====================================================================

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    """Função chamada quando o cliente MQTT se conecta ao broker."""
    if rc == 0:
        print('Broker Connected successfully')
        mqtt_client.subscribe(topic_subscribe) # Assina o tópico
    else:
        print('Bad connection. Code:', rc)

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    """Função chamada ao receber uma mensagem em um tópico assinado."""
    # A variável 'app' é acessível após ser retornada por create_app()
    app = create_app() 
    
    if (message.topic == topic_subscribe):
        js = json.loads(message.payload.decode())
        
        try:
            # Garante que a operação de BD ocorra no contexto da aplicação
            with app.app_context():
                # Assumimos que o JSON tem chaves 'sensor' (topic) e 'valor' (value)
                Read.save_read(js["sensor"], js["valor"]) 
        except Exception as e:
            # print(f"Erro ao salvar leitura: {e}") 
            pass