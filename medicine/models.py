from django.db import models
from django.db.models import Avg
from django.utils.translation import gettext as _
from multiselectfield import MultiSelectField

from medicine import constants


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
    diagnosis = models.ForeignKey(to='medicine.Diagnosis', on_delete=models.CASCADE, null=True, blank=True,
                                  editable=False)

    class Meta:
        verbose_name = _('statistics')
        verbose_name_plural = _('statistics')


class Diagnosis(models.Model):
    HIGH_BLOOD_PRESSURE = 'high_blood_pressure'
    LOW_BLOOD_PRESSURE = 'low_blood_pressure'
    HIGH_GLUCOSE = 'high_glucose'
    LOW_GLUCOSE = 'high_glucose'
    HIGH_PROTEIN = 'high_protein'
    LOW_PROTEIN = 'low_protein'
    HIGH_ALBUMIN = 'high_albumin'
    LOW_ALBUMIN = 'low_albumin'
    HIGH_MYOGLOBIN = 'high_myoglobin'
    LOW_MYOGLOBIN = 'low_myoglobin'
    HIGH_FERRITIN = 'high_ferritin'
    LOW_FERRITIN = 'low_ferritin'
    HIGH_TEMPERATURE = 'high_temperature'
    GOOD_HEALTH = 'good_health'

    VERDICT_CHOICES = (
        (HIGH_BLOOD_PRESSURE, constants.HIGH_BLOOD_PRESSURE_ADVICE),
        (LOW_BLOOD_PRESSURE, constants.LOW_BLOOD_PRESSURE_ADVICE),
        (HIGH_GLUCOSE, constants.HIGH_GLUCOSE_ADVICE),
        (LOW_GLUCOSE, constants.LOW_BLOOD_PRESSURE_ADVICE),
        (HIGH_PROTEIN, constants.HIGH_PROTEIN_ADVICE),
        (LOW_PROTEIN, constants.LOW_PROTEIN_ADVICE),
        (HIGH_ALBUMIN, constants.HIGH_ALBUMIN_ADVICE),
        (LOW_ALBUMIN, constants.LOW_ALBUMIN_ADVICE),
        (HIGH_MYOGLOBIN, constants.HIGH_MYOGLOBIN_ADVICE),
        (LOW_MYOGLOBIN, constants.LOW_MYOGLOBIN_ADVICE),
        (HIGH_FERRITIN, constants.HIGH_FERRITIN_ADVICE),
        (LOW_FERRITIN, constants.LOW_FERRITIN_ADVICE),
        (HIGH_TEMPERATURE, constants.HIGH_TEMPERATURE_ADVICE),
        (HIGH_TEMPERATURE, constants.HIGH_TEMPERATURE_ADVICE),
        (GOOD_HEALTH, constants.GOOD_HEALTH),
    )

    verdict = PatchedMultiSelectField(verbose_name=_('verdict'), choices=VERDICT_CHOICES)
    start_time = models.DateTimeField(verbose_name=_('start time'), editable=False)
    end_time = models.DateTimeField(verbose_name=_('end time'), editable=False)
    user = models.ForeignKey(to='core.User', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('diagnosis')
        verbose_name_plural = _('diagnosis')

    def get_verdict(self, statistics):
        self.statistics_set.set(statistics)
        avg_data = statistics.aggregate(Avg('min_blood_pressure'), Avg('max_blood_pressure'), Avg('glucose_rate'),
                                        Avg('protein_rate'), Avg('albumin_rate'), Avg('myoglobin_rate'),
                                        Avg('ferritin_rate'), Avg('cholesterol_rate'), Avg('temperature'))
        verdict = []

        for age, values in constants.HEART_PRESSURE[self.user.gender].items():
            if self.user.age < age:
                min_blood_pressure = avg_data['min_blood_pressure__avg'] - values['norm_min']
                max_blood_pressure = avg_data['max_blood_pressure__avg'] - values['norm_max']
                pressure_diff = (min_blood_pressure + max_blood_pressure) / 2
                if pressure_diff <= -10:
                    verdict.append(self.LOW_BLOOD_PRESSURE)
                elif pressure_diff >= 10:
                    verdict.append(self.HIGH_BLOOD_PRESSURE)
                break

        for age, values in constants.GLUCOSE_RATE.items():
            if self.user.age < age:
                if avg_data['glucose_rate__avg'] < values['norm_min']:
                    verdict.append(self.LOW_GLUCOSE)
                elif avg_data['glucose_rate__avg'] > values['norm_max']:
                    verdict.append(self.HIGH_GLUCOSE)
                break

        for age, values in constants.PROTEIN_RATE.items():
            if self.user.age < age:
                if avg_data['protein_rate__avg'] < values['norm_min']:
                    verdict.append(self.LOW_PROTEIN)
                elif avg_data['protein_rate__avg'] > values['norm_max']:
                    verdict.append(self.HIGH_PROTEIN)
                break

        for age, values in constants.ALBUMIN_RATE.items():
            if self.user.age < age:
                if avg_data['albumin_rate__avg'] < values['norm_min']:
                    verdict.append(self.LOW_ALBUMIN)
                elif avg_data['albumin_rate__avg'] > values['norm_max']:
                    verdict.append(self.HIGH_ALBUMIN)
                break

        if avg_data['myoglobin_rate__avg'] < constants.MYOGLOBIN_RATE[self.user.gender]['norm_min']:
            verdict.append(self.LOW_MYOGLOBIN)
        elif avg_data['myoglobin_rate__avg'] > constants.MYOGLOBIN_RATE[self.user.gender]['norm_max']:
            verdict.append(self.HIGH_MYOGLOBIN)

        if avg_data['ferritin_rate__avg'] < constants.FERRITIN_RATE[self.user.gender]['norm_min']:
            verdict.append(self.LOW_FERRITIN)
        elif avg_data['ferritin_rate__avg'] > constants.FERRITIN_RATE[self.user.gender]['norm_max']:
            verdict.append(self.HIGH_FERRITIN)

        elif avg_data['temperature__avg'] - constants.TEMPERATURE >= 1:
            verdict.append(self.HIGH_TEMPERATURE)
        if not len(verdict):
            verdict.append(self.GOOD_HEALTH)
        self.verdict = verdict


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
        (MONDAY, _('monday')),
        (TUESDAY, _('tuesday')),
        (WEDNESDAY, _('wednesday')),
        (THURSDAY, _('thursday')),
        (FRIDAY, _('friday')),
        (SATURDAY, _('saturday')),
        (SUNDAY, _('sunday')),
        (EVERYDAY, _('everyday'))
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
