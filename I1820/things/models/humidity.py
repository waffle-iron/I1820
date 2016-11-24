# In The Name Of God
# ========================================
# [] File Name : humidity.py
#
# [] Creation Date : 10-09-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
# =======================================
from ..sensor import SensorThing
from ..types import State


class Humidity(SensorThing):
    """
    This class represents Humidity sensor
    """
    name = "humidity"

    humidity = State()

    def __init__(self, agent_id, device_id):
        super().__init__(agent_id, device_id)
