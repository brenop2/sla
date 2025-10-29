# models/iot/write.py
# Diretório: EXEMPLO2/models/iot/

from models.db import db
from models.iot.actuators import Actuator
from models.iot.devices import Device
from datetime import datetime

class Write(db.Model):
    __tablename__ = 'write'
    
    id = db.Column('id', db.Integer, nullable=False, primary_key=True)
    write_datetime = db.Column(db.DateTime(), nullable=False)
    actuators_id = db.Column(db.Integer, db.ForeignKey(Actuator.id), nullable=False)
    value = db.Column(db.Float, nullable=True)

    @classmethod
    def save_write(cls, actuator_id, value):
        """Salva um novo comando de atuação no banco de dados."""
        actuator = Actuator.query.filter(Actuator.id == actuator_id).first()
        
        if actuator is not None: 
            write = cls(write_datetime=datetime.now(), actuators_id=actuator.id, value=float(value))
            db.session.add(write)
            db.session.commit()

    @classmethod
    def get_writes(cls, device_id, start, end):
        """Retorna o histórico de comandos de um atuador dentro de um período."""
        actuator = Actuator.query.filter(Actuator.devices_id == device_id).first()
        
        if actuator: 
            writes = cls.query.filter(cls.actuators_id == actuator.id, 
                                      cls.write_datetime > start, 
                                      cls.write_datetime < end).all()
            return writes
        return []