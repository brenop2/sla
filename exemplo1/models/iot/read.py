# models/iot/read.py
# Diretório: EXEMPLO2/models/iot/

from models.db import db
from models.iot.sensors import Sensor
from models.iot.devices import Device
from datetime import datetime

class Read(db.Model):
    __tablename__ = 'read'
    
    id = db.Column('id', db.Integer, nullable=False, primary_key=True)
    read_datetime = db.Column(db.DateTime(), nullable=False)
    sensors_id = db.Column(db.Integer, db.ForeignKey(Sensor.id), nullable=False)
    value = db.Column(db.Float, nullable=True)

    @classmethod
    def save_read(cls, topic, value):
        """Salva uma nova leitura se o dispositivo estiver ativo."""
        sensor = Sensor.query.filter(Sensor.topic == topic).first()
        
        if sensor is not None: 
            device = Device.query.filter(Device.id == sensor.devices_id).first()
            
            if (device is not None) and (device.is_active == True): 
                read = cls(read_datetime=datetime.now(), sensors_id=sensor.id, value=float(value))
                db.session.add(read)
                db.session.commit()

    @classmethod
    def get_read(cls, device_id, start, end):
        """Retorna leituras históricas de um sensor dentro de um período."""
        sensor = Sensor.query.filter(Sensor.devices_id == device_id).first()
        
        if sensor: 
            read = cls.query.filter(cls.sensors_id == sensor.id, 
                                      cls.read_datetime > start, 
                                      cls.read_datetime < end).all()
            return read
        return []