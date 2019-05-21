import json
import logging
from json import JSONDecodeError

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
        try:
            Statistics.objects.create(**json.loads(data.decode()))
        except TypeError as e:
            logger.error(e)
        except JSONDecodeError as e:
            logger.error(e)
