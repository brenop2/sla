# controllers/write_controller.py
from flask import Blueprint, request, render_template
from models.iot.write import Write
from models.iot.actuators import Actuator
from datetime import datetime

write = Blueprint("write", __name__, template_folder="views")

# Rota para exibir os dados históricos dos atuadores
@write.route("/history_write", methods=["GET", "POST"])
def history_write():
    # Se o método for POST, pega os dados do formulário
    if request.method == "POST":
        actuator_id = request.form["actuator_id"]
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        # Converte as datas de string para datetime, se forem fornecidas
        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

        # Obtém os dados históricos de atuação
        historical_data = Write.get_historical_data(actuator_id, start_date, end_date)

        # Obtém todos os atuadores
        actuators = Actuator.query.all()

        return render_template("history_write.html", historical_data=historical_data, actuators=actuators)

    else:
        # Se GET, apenas exibe os atuadores disponíveis
        actuators = Actuator.query.all()
        return render_template("history_write.html", actuators=actuators)
