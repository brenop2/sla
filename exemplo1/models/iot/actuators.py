# models/iot/actuators.py
# Diretório: EXEMPLO2/models/iot/

from models.db import db
from models.iot.devices import Device

class Actuator(db.Model):
    __tablename__ = 'actuators'
    
    id = db.Column('id', db.Integer, primary_key=True)
    devices_id = db.Column(db.Integer, db.ForeignKey(Device.id))
    unit = db.Column(db.String(50))
    topic = db.Column(db.String(50))
    
    @classmethod
    def save_actuator(cls, name, brand, model, topic, unit, is_active):
        """Cria e salva um novo dispositivo e atuador."""
        device = Device(name=name, brand=brand, model=model, is_active=is_active)
        actuator = cls(unit=unit, topic=topic)
        
        device.actuators.append(actuator) 
        
        db.session.add(device)
        db.session.commit()

    @classmethod
    def get_actuators(cls):
        """Recupera todos os atuadores com dados do dispositivo."""
        actuators = cls.query.join(Device, Device.id == cls.devices_id)\
            .add_columns(Device.id, Device.name, Device.brand, Device.model,\
                         Device.is_active, cls.topic, cls.unit).all()
        return actuators
        
    @classmethod
    def get_single_actuator(cls, id):
        """Busca um único atuador para edição."""
        actuator = cls.query.filter(cls.devices_id == id)\
            .join(Device)\
            .add_columns(Device.id, Device.name, Device.brand, Device.model,\
                         Device.is_active, cls.topic, cls.unit)\
            .first()
        return [actuator] if actuator is not None else []

    @classmethod
    def update_actuator(cls, id, name, brand, model, topic, unit, is_active):
        """Atualiza um registro de dispositivo e atuador."""
        device = Device.query.filter(Device.id == id).first()
        actuator = cls.query.filter(cls.devices_id == id).first()
        
        if device is not None:
            device.name = name
            device.brand = brand
            device.model = model
            actuator.topic = topic
            actuator.unit = unit
            device.is_active = is_active
            db.session.commit()
            
        return cls.get_actuators()

    @classmethod
    def delete_actuator(cls, id):
        """Exclui um registro de atuador e seu dispositivo associado."""
        device = Device.query.filter(Device.id == id).first()
        actuator = cls.query.filter(cls.devices_id == id).first()
        
        if actuator is not None and device is not None:
            # Note: A exclusão em cascata deve ser gerenciada pelo DB ou adicionada aqui.
            db.session.delete(actuator)
            db.session.delete(device)
            db.session.commit()
            
        return cls.get_actuators()