# controllers/actuators_controller.py
# Diretório: EXEMPLO2/controllers/

from flask import Blueprint, request, render_template, redirect, url_for
from models.iot.actuators import Actuator
from models.iot.write import Write

actuator_ = Blueprint("actuator_", __name__, template_folder="views")

@actuator_.route('/register_actuator')
def register_actuator():
    return render_template("register_actuator.html")

@actuator_.route('/add_actuator', methods=['POST'])
def add_actuator():
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    is_active = True if request.form.get("is_active") == "on" else False
    
    Actuator.save_actuator(name, brand, model, topic, unit, is_active)
    
    return redirect(url_for('actuator_.actuators'))

@actuator_.route('/actuators')
def actuators():
    actuators = Actuator.get_actuators()
    return render_template("actuators.html", actuators=actuators)

@actuator_.route('/edit_actuator')
def edit_actuator():
    id = request.args.get('id', None)
    actuator = Actuator.get_single_actuator(id)
    return render_template("update_actuator.html", actuator=actuator[0] if actuator else None)

@actuator_.route('/update_actuator', methods=['POST'])
def update_actuator():
    id = request.form.get("id")
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    is_active = True if request.form.get("is_active") == "on" else False
    
    Actuator.update_actuator(id, name, brand, model, topic, unit, is_active)
    return redirect(url_for('actuator_.actuators'))

@actuator_.route('/del_actuator', methods=['GET'])
def del_actuator():
    id = request.args.get('id', None)
    Actuator.delete_actuator(id)
    return redirect(url_for('actuator_.actuators'))

@actuator_.route("/history_write")
def history_write():
    actuators = Actuator.get_actuators()
    writes = {}
    return render_template("history_write.html", actuators=actuators, writes=writes)

@actuator_.route("/get_write", methods=['POST'])
def get_write():
    if request.method == 'POST':
        id = request.form['id']
        start = request.form['start']
        end = request.form['end']
        
        writes = Write.get_writes(id, start, end)
        actuators = Actuator.get_actuators()
        
        return render_template("history_write.html", actuators=actuators, writes=writes)