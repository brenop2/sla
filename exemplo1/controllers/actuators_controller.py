from flask import Blueprint, render_template, request
from models import db
from models.iot.devices import Device
from models.iot.actuators import Actuator

actuator_ = Blueprint("actuator_", __name__, template_folder="views")

# Registra o blueprint de atuadores
# Em app.py, o blueprint já está registrado com app.register_blueprint(actuator_, url_prefix="/")

# Rota para exibir os atuadores
@actuator_.route("/list_actuators")
def list_actuators():
    actuators = get_actuators()  # Chama a função para obter os atuadores
    return render_template("list_actuators.html", actuators=actuators)


# Função para pegar os atuadores e seus dispositivos
def get_actuators():
    actuators = (
        Actuator.query.join(Device, Device.id == Actuator.devices_id)
        .add_columns(
            Device.id,
            Device.name,
            Device.brand,
            Device.model,
            Device.is_active,
            Actuator.unit,
            Actuator.topic,
        )
        .all()
    )
    return actuators


# Rota para o formulário de cadastro de atuadores
@actuator_.route("/register_actuator")
def register_actuator():
    return render_template("register_actuator.html")  # Formulário de registro de atuador


# Rota para adicionar um atuador no banco de dados
@actuator_.route("/add_actuator", methods=["POST"])
def add_actuator():
    # Coleta os dados do formulário
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    is_active = True if request.form.get("is_active") == "on" else False

    # Chama a função save_actuator para salvar no banco de dados
    save_actuator(name, brand, model, topic, unit, is_active)

    actuators = get_actuators()
    return render_template("actuators.html", actuators=actuators)


# Função para salvar o dispositivo (device) e atuador no banco de dados
def save_actuator(name, brand, model, topic, unit, is_active):
    # Cria um novo dispositivo (device)
    device = Device(name=name, brand=brand, model=model, is_active=is_active)

    # Adiciona o dispositivo ao banco de dados
    db.session.add(device)
    db.session.commit()  # Comita para garantir que o dispositivo seja salvo no banco

    # Cria um novo atuador, associando ao dispositivo (device) recém-criado
    actuator = Actuator(devices_id=device.id, unit=unit, topic=topic)

    # Adiciona o atuador ao banco de dados
    db.session.add(actuator)
    db.session.commit()  # Comita para garantir que o atuador seja salvo no banco de dados
