# models/iot/devices.py
# Diretório: EXEMPLO2/models/iot/

from models.db import db

class Device(db.Model):
    __tablename__ = 'devices'
    
    # Colunas da tabela 'devices'
    id = db.Column('id', db.Integer, primary_key=True) 
    name = db.Column(db.String(50))
    brand = db.Column(db.String(50))
    model = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, nullable=False, default=False) 
    
    # Relacionamentos
    sensors = db.relationship('Sensor', backref='devices', lazy=True)
    actuators = db.relationship('Actuator', backref='devices', lazy=True)
    
    def __repr__(self):
        return f"Device(id={self.id}, name='{self.name}')"