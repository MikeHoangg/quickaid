import json
import logging

import serial

from medicine.models import Statistics

logger = logging.getLogger('get_statistics_logger')

# TODO give permissions each time to the right port
# sudo adduser USERNAME dialout
# sudo chmod a+rw /dev/ttyUSB*
IOT_PORT = '/dev/ttyUSB0'


def get_iot_data():
    ser = serial.Serial(port=IOT_PORT, baudrate=9600, timeout=60)
    data = ser.readline()
    if data:
        logger.info(data)
        stats = Statistics.objects.create(**json.loads(data.decode()))
        stats.get_diagnosis()
    ser.close()
