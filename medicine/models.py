from django.db import models
from django.utils.translation import gettext as _
from multiselectfield import MultiSelectField


class PatchedMultiSelectField(MultiSelectField):
    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)


class Statistics(models.Model):
    min_blood_pressure = models.PositiveIntegerField(verbose_name=_('min pressure'))
    max_blood_pressure = models.PositiveIntegerField(verbose_name=_('max pressure'))
    glucose_rate = models.FloatField(verbose_name=_('glucose rate'))
    protein_rate = models.FloatField(verbose_name=_('protein rate'))
    albumin_rate = models.FloatField(verbose_name=_('albumin rate'))
    myoglobin_rate = models.FloatField(verbose_name=_('myoglobin rate'))
    ferritin_rate = models.FloatField(verbose_name=_('ferritin rate'))
    cholesterol_rate = models.FloatField(verbose_name=_('cholesterol rate'))
    temperature = models.FloatField(verbose_name=_('temperature'))
    created = models.DateTimeField(verbose_name='created', auto_now_add=True, editable=False)
    user = models.ForeignKey(to='core.User', on_delete=models.CASCADE)

    def get_diagnosis(self):
        pass

    class Meta:
        verbose_name = _('statistics')
        verbose_name_plural = _('statistics')


class Diagnosis(models.Model):
    verdict = models.TextField(verbose_name=_('verdict'))
    created = models.DateTimeField(verbose_name='created', auto_now_add=True, editable=False)
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
    days = PatchedMultiSelectField(verbose_name=_('days'), choices=DAYS_CHOICES, min_choices=1)
    active = models.BooleanField(verbose_name=_('active'), default=True)
    user = models.ForeignKey(verbose_name=_('user'), to='core.User', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('schedule')
        verbose_name_plural = _('schedules')


class Notification(models.Model):
    schedule = models.ForeignKey(verbose_name=_('schedule'), to='medicine.Schedule', on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='created', auto_now_add=True, editable=False)
    pending = models.BooleanField(verbose_name=_('pending'), default=True)

    class Meta:
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')
