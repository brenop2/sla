from flask import Blueprint, request, render_template
from models import db
from models.iot.sensors import Sensor
from models.iot.devices import Device

sensor_ = Blueprint("sensor_", __name__, template_folder="views")

# Rota para o formulário de cadastro de sensores
@sensor_.route("/register_sensor")
def register_sensor():
    return render_template("register_sensor.html")  # Formulário de registro de sensor

# Função para pegar os sensores e seus dispositivos
def get_sensors():
    sensors = (
        Sensor.query.join(Device, Device.id == Sensor.devices_id)
        .add_columns(
            Device.id,
            Device.name,
            Device.brand,
            Device.model,
            Device.is_active,
            Sensor.topic,
            Sensor.unit,
        )
        .all()
    )
    return sensors

# Rota para exibir os sensores
@sensor_.route("/list_sensors")
def list_sensors():
    sensors = get_sensors()  # Chama a função para obter os sensores
    return render_template("list_sensors.html", sensors=sensors)

# Rota para adicionar um sensor no banco de dados
@sensor_.route("/add_sensor", methods=["POST"])
def add_sensor():
    # Coleta os dados do formulário
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    is_active = True if request.form.get("is_active") == "on" else False

    # Chama a função save_sensor para salvar no banco de dados
    save_sensor(name, brand, model, topic, unit, is_active)

    sensors = get_sensors()
    return render_template("sensors.html", sensors=sensors)

# Função para salvar o dispositivo (device) e sensor no banco de dados
def save_sensor(name, brand, model, topic, unit, is_active):
    # Cria um novo dispositivo (device)
    device = Device(name=name, brand=brand, model=model, is_active=is_active)

    # Adiciona o dispositivo ao banco de dados
    db.session.add(device)
    db.session.commit()  # Comita para garantir que o dispositivo seja salvo no banco

    # Cria um novo sensor, associando ao dispositivo (device) recém-criado
    sensor = Sensor(devices_id=device.id, unit=unit, topic=topic)

    # Adiciona o sensor ao banco de dados
    db.session.add(sensor)
    db.session.commit()  # Comita para garantir que o sensor seja salvo no banco de dados

# Editar Sensor - Rota para exibir o formulário de edição
@sensor_.route('/edit_sensor')
def edit_sensor():
    id = request.args.get('id', None)
    sensor = Sensor.get_single_sensor(id)
    return render_template("update_sensor.html", sensor=sensor)

# Método para obter os dados do sensor selecionado para edição
def get_single_sensor(id):
    sensor = Sensor.query.filter(Sensor.devices_id == id).first()
    if sensor:
        sensor = Sensor.query.filter(Sensor.devices_id == id).join(Device).add_columns(
            Device.id, Device.name, Device.brand, Device.model, Device.is_active, Sensor.topic, Sensor.unit).first()
    return [sensor]

# Atualizar o sensor no banco de dados
@sensor_.route('/update_sensor', methods=['POST'])
def update_sensor():
    id = request.form.get("id")
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    is_active = True if request.form.get("is_active") == "on" else False

    sensors = Sensor.update_sensor(id, name, brand, model, topic, unit, is_active)
    return render_template("sensors.html", sensors=sensors)

# Método para atualizar o sensor no modelo
def update_sensor(id, name, brand, model, topic, unit, is_active):
    device = Device.query.filter(Device.id == id).first()
    sensor = Sensor.query.filter(Sensor.devices_id == id).first()
    if device:
        device.name = name
        device.brand = brand
        device.model = model
        sensor.topic = topic
        sensor.unit = unit
        device.is_active = is_active
        db.session.commit()
    return Sensor.get_sensors()
