import json
import logging
import random
from json import JSONDecodeError

import serial

from medicine.models import Statistics

logger = logging.getLogger('get_statistics_logger')

# TODO give permissions each time to the right port
# sudo adduser USERNAME dialout
# sudo chmod a+rw /dev/ttyUSB*
IOT_PORT = '/dev/ttyUSB0'


def get_iot_data():
    ser = serial.Serial(port=IOT_PORT, baudrate=9600, timeout=300)
    data = ser.readline()
    if data:
        logger.info(data)
        try:
            Statistics.objects.create(**json.loads(data.decode()))
        except TypeError as e:
            logger.error(e)
        except JSONDecodeError as e:
            logger.error(e)


def get_random_statistics():
    data = {}
    heart_rate_1 = random.randint(60, 170)
    heart_rate_2 = random.randint(60, 170)
    data.update({
        "max_blood_pressure": heart_rate_1 if heart_rate_1 > heart_rate_2 else heart_rate_2,
        "min_blood_pressure": heart_rate_1 if heart_rate_1 < heart_rate_2 else heart_rate_2,
        "glucose_rate": random.uniform(2, 8),
        "protein_rate": random.randint(50, 90),
        "albumin_rate": random.randint(10, 60),
        "myoglobin_rate": random.randint(10, 90),
        "ferritin_rate": random.randint(10, 130),
        "cholesterol_rate": random.randint(1, 10),
        "temperature": random.uniform(34, 43),
        "user_id": 2
    })

    logger.info(data)
    Statistics.objects.create(**data)
