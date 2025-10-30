from models.db import db
from models.iot.devices import Device


class Actuator(db.Model):
    __tablename__ = "actuators"

    id = db.Column("id", db.Integer, primary_key=True)
    devices_id = db.Column(
        db.Integer, db.ForeignKey(Device.id)
    )  # Relacionamento com a tabela devices
    unit = db.Column(db.String(50))
    topic = db.Column(db.String(50))

    # Método estático para retornar todos os atuadores com dados adicionais do dispositivo
    @staticmethod
    def get_actuators():
        return (
            Actuator.query.join(Device, Device.id == Actuator.devices_id)
            .add_columns(
                Device.id,
                Device.name,
                Device.brand,
                Device.model,
                Device.is_active,
                Actuator.topic,
                Actuator.unit,
            )
            .all()
        )
