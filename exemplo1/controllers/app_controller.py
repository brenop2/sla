# app_controller.py
import json

from flask import Blueprint, Flask, render_template
from flask_mqtt import Mqtt

from models.db import db, instance
from models.iot.actuators import Actuator

actuator_ = Blueprint("actuator_", __name__, template_folder="views")


@actuator_.route("/list_actuators")
def list_actuators():
    actuators = (
        Actuator.get_actuators()
    )  # Chama o método para pegar os atuadores com dados do dispositivo
    return render_template("list_actuators.html", actuators=actuators)


def create_app():
    app = Flask(
        __name__, template_folder="./views/", static_folder="./static/", root_path="./"
    )

    app.config["TESTING"] = False
    app.config["SECRET_KEY"] = "generated-secrete-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = instance
    db.init_app(app)

    @app.route("/")
    def index():
        return render_template("home.html")

    return app


app.config["MQTT_BROKER_URL"] = "mqtt-dashboard.com"
app.config["MQTT_BROKER_PORT"] = 1883
app.config["MQTT_USERNAME"] = ""
app.config["MQTT_PASSWORD"] = ""
app.config["MQTT_KEEPALIVE"] = 5000
app.config["MQTT_TLS_ENABLED"] = False
mqtt_client = Mqtt()
mqtt_client.init_app(app)
topic_subscribe = "/aula_flask/"


@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Broker Connected successfully")
        mqtt_client.subscribe(topic_subscribe)  # subscribe topic
    else:
        print("Bad connection. Code:", rc)


@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    if message.topic == topic_subscribe:
        js = json.loads(message.payload.decode())
        try:
            with app.app_context():
                Read.save_read(js["sensor"], js["valor"])
        except:
            pass
