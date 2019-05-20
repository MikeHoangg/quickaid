from celery.schedules import crontab

from medicine.utils import get_iot_data
from quickaid.celery import app


@app.task(name='get_statistics')
def get_statistics():
    """
    Task to get statistics for certain user
    :return:
    """
    get_iot_data()


schedule = {
    'get_statistics': {
        'task': 'get_statistics',
        'schedule': crontab(minute="*/1")
        # 'schedule': crontab(minute=0, hour='*/1')
    }
}

app.conf.beat_schedule = schedule
