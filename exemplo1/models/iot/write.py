# models/iot/write.py
from models.db import db
from datetime import datetime

class Write(db.Model):
    __tablename__ = 'write'

    id = db.Column('id', db.Integer, primary_key=True)
    write_datetime = db.Column(db.DateTime(), nullable=False)
    value = db.Column(db.Float, nullable=True)
    actuators_id = db.Column(db.Integer, db.ForeignKey('actuators.id'), nullable=False)

    # Método para salvar a atuação na tabela 'write'
    @staticmethod
    def save_write(actuators_id, value):
        write = Write(
            write_datetime=datetime.now(),
            actuators_id=actuators_id,
            value=value
        )
        db.session.add(write)
        db.session.commit()

    # Método para obter todos os históricos de atuações de um atuador específico
    @staticmethod
    def get_historical_data(actuator_id, start_date=None, end_date=None):
        query = Write.query.filter(Write.actuators_id == actuator_id)

        if start_date:
            query = query.filter(Write.write_datetime >= start_date)
        if end_date:
            query = query.filter(Write.write_datetime <= end_date)

        return query.all()
