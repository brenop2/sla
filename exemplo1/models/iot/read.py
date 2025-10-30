# models/iot/read.py
from datetime import datetime

from models.db import db
from models.iot.sensors import Sensor


class Read(db.Model):
    __tablename__ = "read"

    id = db.Column("id", db.Integer, nullable=False, primary_key=True)
    read_datetime = db.Column(db.DateTime(), nullable=False)
    sensors_id = db.Column(db.Integer, db.ForeignKey(Sensor.id), nullable=False)
    value = db.Column(db.Float, nullable=True)


# Método para salvar a leitura no banco
def save_read(topic, value):
    sensor = Sensor.query.filter(Sensor.topic == topic).first()
    device = Device.query.filter(Device.id == sensor.devices_id).first()
    if sensor and device.is_active:
        read = Read(
            read_datetime=datetime.now(), sensors_id=sensor.id, value=float(value)
        )
        db.session.add(read)
        db.session.commit()
