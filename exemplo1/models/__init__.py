# models/__init__.py
# Diretório: EXEMPLO2/models/

from models.db import db
# Modelos IoT
from models.iot.devices import Device
from models.iot.sensors import Sensor
from models.iot.actuators import Actuator
from models.iot.read import Read
from models.iot.write import Write
# Modelos de Usuário
from models.user.roles import Role 
from models.user.users import User