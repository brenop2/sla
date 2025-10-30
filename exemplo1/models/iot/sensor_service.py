from models.iot.sensors import Sensor
from models.iot.devices import Device

def get_sensors():
    sensors = Sensor.query.join(Device, Device.id == Sensor.devices_id)\
        .add_columns(Device.id, Device.name, Device.brand, Device.model, 
                     Device.is_active, Sensor.topic, Sensor.unit).all()
    return sensors
