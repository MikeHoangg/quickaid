from rest_framework import serializers, fields

from medicine.models import Statistics, Diagnosis, Schedule, Notification


class DiagnosisSerializer(serializers.HyperlinkedModelSerializer):
    def get_verdict(self, obj):
        return obj.get_verdict_display()

    class Meta:
        model = Diagnosis
        fields = ('id', 'url', 'verdict', 'start_time', 'end_time')


class StatisticsSerializer(serializers.HyperlinkedModelSerializer):
    diagnosis = DiagnosisSerializer()

    class Meta:
        model = Statistics
        fields = ('id', 'url', 'diagnosis', 'min_blood_pressure', 'max_blood_pressure', 'glucose_rate', 'protein_rate',
                  'albumin_rate', 'myoglobin_rate', 'ferritin_rate', 'cholesterol_rate', 'temperature', 'created')


class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    days = fields.MultipleChoiceField(choices=Schedule.DAYS_CHOICES, allow_blank=False)

    class Meta:
        model = Schedule
        fields = ('id', 'url', 'reason', 'description', 'expiration_date', 'time', 'days', 'active')

    def save(self, **kwargs):
        self.validated_data.update({'user': kwargs.get('user')})
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
