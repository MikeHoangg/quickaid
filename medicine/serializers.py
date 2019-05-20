from rest_framework import serializers, fields

from core.models import User
from medicine.models import Statistics, Diagnosis, Schedule, Notification


class DiagnosisSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Diagnosis
        fields = ('id', 'url', 'statistics', 'verdict', 'created')


class StatisticsSerializer(serializers.HyperlinkedModelSerializer):
    diagnosis_set = DiagnosisSerializer(many=True)

    class Meta:
        model = Statistics
        fields = ('id', 'url', 'min_blood_pressure', 'max_blood_pressure', 'glucose_rate', 'protein_rate', 'albumin_rate',
                  'myoglobin_rate', 'ferritin_rate', 'cholesterol_rate', 'temperature', 'created', 'diagnosis_set')


class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    days = fields.MultipleChoiceField(choices=Schedule.DAYS_CHOICES, allow_blank=False)

    class Meta:
        model = Schedule
        fields = ('id', 'url', 'reason', 'description', 'expiration_date', 'time', 'days', 'active')

    def save(self, **kwargs):
        self.validated_data.update({'user': User.objects.last()})
        return super().save()


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    schedule = ScheduleSerializer()

    class Meta:
        model = Notification
        fields = ('id', 'url', 'created', 'pending', 'schedule')

    def update(self, instance, validated_data):
        instance.pending = False
        instance.save()
        return instance
