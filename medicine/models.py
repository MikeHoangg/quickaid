from django.db import models
from django.utils.translation import gettext as _
from multiselectfield import MultiSelectField


class Statistics(models.Model):
    min_heart_rate = models.PositiveIntegerField(verbose_name=_('min heart rate'))
    max_heart_rate = models.PositiveIntegerField(verbose_name=_('max heart rate'))
    glucose_rate = models.FloatField(verbose_name=_('glucose rate'))
    protein_rate = models.FloatField(verbose_name=_('protein rate'))
    albumin_rate = models.FloatField(verbose_name=_('albumin rate'))
    myoglobin_rate = models.FloatField(verbose_name=_('myoglobin rate'))
    ferritin_rate = models.FloatField(verbose_name=_('ferritin rate'))
    cholesterol_rate = models.FloatField(verbose_name=_('cholesterol rate'))
    temperature = models.FloatField(verbose_name=_('temperature'))
    created = models.DateTimeField(verbose_name='created', auto_created=True, editable=False)
    user = models.ForeignKey(to='core.User', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('statistics')
        verbose_name_plural = _('statistics')


class Diagnosis(models.Model):
    verdict = models.TextField(verbose_name=_('verdict'))
    created = models.DateTimeField(verbose_name='created', auto_created=True, editable=False)
    statistics = models.ForeignKey(to='medicine.Statistics', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('diagnosis')
        verbose_name_plural = _('diagnosis')


class Schedule(models.Model):
    MONDAY = 'mon'
    TUESDAY = 'tue'
    WEDNESDAY = 'wed'
    THURSDAY = 'thu'
    FRIDAY = 'fri'
    SATURDAY = 'sat'
    SUNDAY = 'sun'
    EVERYDAY = 'evr'

    DAYS_CHOICES = (
        (MONDAY, 'monday'),
        (TUESDAY, 'tuesday'),
        (WEDNESDAY, 'wednesday'),
        (THURSDAY, 'thursday'),
        (FRIDAY, 'friday'),
        (SATURDAY, 'saturday'),
        (SUNDAY, 'sunday'),
        (EVERYDAY, 'everyday'),
    )

    reason = models.TextField(verbose_name=_('reason'), null=True, blank=True)
    description = models.TextField(verbose_name=_('description'))
    expiration_date = models.DateField(verbose_name=_('expiration date'), null=True, blank=True)
    time = models.TimeField(verbose_name=_('time'))
    days = MultiSelectField(verbose_name=_('days'), choices=DAYS_CHOICES, min_choices=1)
    active = models.BooleanField(verbose_name=_('active'), default=True)
    user = models.ForeignKey(to='core.User', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('schedule')
        verbose_name_plural = _('schedules')
