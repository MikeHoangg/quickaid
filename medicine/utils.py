import json
import logging
from time import sleep

import serial
logger = logging.getLogger('get_statistics')

from medicine.models import Statistics
# TODO give permissions each time to the right port
# sudo chmod a+rw /dev/ttyUSB*
IOT_PORT = '/dev/ttyUSB0'


def get_iot_data():
    ser = serial.Serial(port=IOT_PORT, baudrate=9600, timeout=1)
    # for i in range(300):
    #     sleep(1)
    #     data = ser.readline()
    #     logger.debug(data)
    #     if data:
    #         Statistics.objects.create(**json.loads(data.decode()))
