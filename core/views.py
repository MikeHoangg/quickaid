from django.contrib.auth import get_user_model, login
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.conf import settings
from rest_auth.app_settings import create_token
from rest_auth.models import TokenModel
from rest_auth.serializers import TokenSerializer
from rest_framework import generics, status, permissions, mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import RegisterSerializer
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@method_decorator(sensitive_post_parameters('password1', 'password2'), name='dispatch')
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny, ]
    token_model = TokenModel

    def _get_response_data(self, user):
        return TokenSerializer(user.auth_token).data

    def _login(self, user, serializer):
        create_token(self.token_model, user, serializer)
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            login(self.request, user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(self._get_response_data(user), status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save()
        self._login(user, serializer)
        return user
