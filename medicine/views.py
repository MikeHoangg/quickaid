from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet

from medicine.models import Statistics, Diagnosis, Schedule, Notification
from medicine.serializers import StatisticsSerializer, DiagnosisSerializer, ScheduleSerializer, NotificationSerializer


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Diagnosis):
            return obj.statistics.user == request.user
        if isinstance(obj, Statistics):
            return obj.user == request.user
        if isinstance(obj, Schedule):
            return obj.user == request.user


class StatisticsViewSet(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Statistics.objects.none()
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = StatisticsSerializer

    def get_queryset(self):
        return Statistics.objects.filter(user=self.request.user)


class DiagnosisViewSet(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Diagnosis.objects.none()
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = DiagnosisSerializer

    def get_queryset(self):
        return Diagnosis.objects.filter(user=self.request.user)


class ScheduleViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Schedule.objects.none()
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        return Schedule.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NotificationViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                          mixins.ListModelMixin, GenericViewSet):
    queryset = Notification.objects.none()
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(schedule__user=self.request.user)

