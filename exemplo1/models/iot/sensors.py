from models.db import db
from models.iot.devices import Device


class Sensor(db.Model):
    __tablename__ = "sensors"

    id = db.Column("id", db.Integer, primary_key=True)
    devices_id = db.Column(
        db.Integer, db.ForeignKey(Device.id)
    )  # Chave estrangeira para o dispositivo
    unit = db.Column(db.String(50))
    topic = db.Column(db.String(50))

    @staticmethod
    def get_sensors():
        return (
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

    # Deletar Sensor - Rota para excluir o sensor


@sensor_.route("/del_sensor", methods=["GET"])
def del_sensor():
    id = request.args.get("id", None)
    sensors = Sensor.delete_sensor(id)
    return render_template("sensors.html", sensors=sensors)


# Método para deletar o sensor e o dispositivo associados
def delete_sensor(id):
    device = Device.query.filter(Device.id == id).first()
    sensor = Sensor.query.filter(Sensor.devices_id == id).first()

    if sensor:
        db.session.delete(sensor)
    if device:
        db.session.delete(device)
    db.session.commit()

    return Sensor.get_sensors()
