# reads_controller.py
from flask import Blueprint, request

from models.iot.read import Read

read = Blueprint("read", __name__, template_folder="views")


# Rota para salvar leitura no banco
@read.route("/save_read", methods=["POST"])
def save_read():
    topic = request.form.get("topic")
    value = request.form.get("value")
    Read.save_read(topic, value)
    return "Leitura salva com sucesso!"


@read.route("/history_read")
def history_read():
    sensors = Sensor.get_sensors()
    read = {}
    return render_template("history_read.html", sensors=sensors, read=read)


@read.route("/get_read", methods=["POST"])
def get_read():
    if request.method == "POST":
        id = request.form["id"]
        start = request.form["start"]
        end = request.form["end"]
        read = Read.get_read(id, start, end)
        sensors = Sensor.get_sensors()
        return render_template("history_read.html", sensors=sensors, read=read)
