# models/iot/sensors.py
# Diretório: EXEMPLO2/models/iot/

from models.db import db
from models.iot.devices import Device

class Sensor(db.Model):
    __tablename__ = 'sensors'
    
    id = db.Column('id', db.Integer, primary_key=True)
    devices_id = db.Column(db.Integer, db.ForeignKey(Device.id))
    unit = db.Column(db.String(50))
    topic = db.Column(db.String(50))
    
    @classmethod
    def save_sensor(cls, name, brand, model, topic, unit, is_active):
        """Insere um novo dispositivo e sensor."""
        device = Device(name=name, brand=brand, model=model, is_active=is_active)
        sensor = cls(unit=unit, topic=topic) 
        device.sensors.append(sensor)
        db.session.add(device)
        db.session.commit()

    @classmethod
    def get_sensors(cls):
        """Recupera todos os sensores com dados do dispositivo."""
        sensors = cls.query.join(Device, Device.id == cls.devices_id)\
            .add_columns(Device.id, Device.name, Device.brand, Device.model,\
                         Device.is_active, cls.topic, cls.unit).all()
        return sensors

    @classmethod
    def get_single_sensor(cls, id):
        """Busca um único sensor para edição."""
        sensor = cls.query.filter(cls.devices_id == id)\
            .join(Device)\
            .add_columns(Device.id, Device.name, Device.brand, Device.model,\
                         Device.is_active, cls.topic, cls.unit)\
            .first()
        return [sensor] if sensor is not None else []

    @classmethod
    def update_sensor(cls, id, name, brand, model, topic, unit, is_active):
        """Atualiza um registro de dispositivo e sensor."""
        device = Device.query.filter(Device.id == id).first()
        sensor = cls.query.filter(cls.devices_id == id).first()
        
        if device is not None:
            device.name = name
            device.brand = brand
            device.model = model
            sensor.topic = topic
            sensor.unit = unit
            device.is_active = is_active
            db.session.commit()
            
        return cls.get_sensors()

    @classmethod
    def delete_sensor(cls, id):
        """Exclui um registro de sensor e seu dispositivo associado."""
        device = Device.query.filter(Device.id == id).first()
        sensor = cls.query.filter(cls.devices_id == id).first()
        
        if sensor is not None and device is not None:
            db.session.delete(sensor)
            db.session.delete(device)
            db.session.commit()
            
        return cls.get_sensors()