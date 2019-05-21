from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _
from rest_framework import serializers, exceptions

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    gender = serializers.SerializerMethodField()

    def get_gender(self, obj):
        return _(obj.get_gender_display())

    class Meta:
        model = User
        fields = ('id', 'url', 'email', 'age', 'gender', 'first_name', 'last_name')


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def authenticate(self, **kwargs):
        return authenticate(request=self.context['request'], **kwargs)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        if User.objects.filter(email__iexact=attrs['email']).exists():
            raise serializers.ValidationError(_("User with such email already exists."))
        return attrs

    def create(self, validated_data):
        credentials = {'email': validated_data['email'], 'password': validated_data['password1']}
        user = User.objects.create(**credentials)
        self.authenticate(**credentials)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **kwargs):
        return authenticate(request=self.context['request'], **kwargs)

    def _validate_username_email(self, email, password):
        if not email or not password:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)
        return self.authenticate(email=email, password=password)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        email = attrs.get('email')
        password = attrs.get('password')
        user = self._validate_username_email(email, password)
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
            attrs['user'] = user
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)
        return attrs

    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        write_only_fields = ('password',)
        read_only_fields = ('id',)
