from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('notifications/<int:user_id>', consumers.NotificationConsumer),
]
