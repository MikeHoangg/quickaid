from django.urls import path, include
from rest_framework import routers

from medicine import views as medicine_views
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'statistics', medicine_views.StatisticsViewSet)
router.register(r'diagnosis', medicine_views.DiagnosisViewSet)
router.register(r'schedule', medicine_views.ScheduleViewSet)
router.register(r'notification', medicine_views.NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('rest_auth.urls')),
    path('register/', views.RegisterView.as_view(), name='register'),
]
