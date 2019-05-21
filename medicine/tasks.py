from datetime import timedelta, datetime

import pytz
from celery.schedules import crontab
from django.contrib.auth import get_user_model
from django.utils import timezone

from medicine.models import Diagnosis, Notification
from medicine.utils import get_iot_data, get_random_statistics
from quickaid.celery import app

User = get_user_model()


@app.task(name='get_statistics')
def get_statistics():
    """
    Task to get statistics for certain user
    :return:
    """
    # get_iot_data()
    get_random_statistics()


@app.task(name='get_diagnosis')
def get_diagnosis():
    """
    Task to get diagnosis for certain user
    :return:
    """
    now = timezone.now()
    end_time = datetime(year=now.year, month=now.month, day=now.day, hour=now.hour, minute=now.minute,
                        second=0).replace(tzinfo=pytz.utc)
    start_time = end_time - timedelta(hours=1)
    for user in User.objects.all():
        statistics = user.statistics_set.filter(created__lte=end_time, created__gte=start_time)
        if statistics.exists():
            diagnosis = Diagnosis.objects.create(user=user, start_time=start_time, end_time=end_time)
            diagnosis.get_verdict(statistics)
            diagnosis.save()


@app.task(name='get_notifications')
def get_notifications():
    """
    Task to get notifications about schedule for certain user
    :return:
    """
    now = timezone.now()
    start_time = datetime(year=now.year, month=now.month, day=now.day, hour=now.hour, minute=now.minute,
                          second=0).replace(tzinfo=pytz.utc)
    end_time = start_time + timedelta(minutes=10)
    today = now.date()
    for user in User.objects.all():
        for sched in user.schedule_set.filter(active=True, expiration_date__lte=today, time__gte=start_time.time(),
                                              time__lte=end_time.time()):
            last = sched.notification_set.order_by('created').last()
            if last and (now - last.created).seconds >= 600 \
                    and (today.weekday() in sched.days or sched.EVERYDAY in sched.days):
                Notification.objects.create(schedule=sched)


schedule = {
    'get_notifications': {
        'task': 'get_notifications',
        'schedule': crontab(minute="*/1")
    },
    'get_statistics': {
        'task': 'get_statistics',
        'schedule': crontab(minute="*/1")
    },
    'get_diagnosis': {
        'task': 'get_diagnosis',
        'schedule': crontab(minute="0", hour="*/1")
    }
}

app.conf.beat_schedule = schedule
