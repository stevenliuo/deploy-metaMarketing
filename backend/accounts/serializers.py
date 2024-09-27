import io
import tempfile
import logging

from django.contrib.auth.password_validation import validate_password
from pptx import Presentation
from rest_framework.serializers import CharField, ModelSerializer, EmailField, FileField, ValidationError
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError

from accounts.models import User, UserSettings
from accounts.exceptions import UserVerificationLinkInvalid
from accounts.tokens import expiring_token_generation, email_expiring_token_generation


logger = logging.getLogger('accounts.serializer')


class UserSettingsSerializer(ModelSerializer):
    """ User settings serializer """

    template_content = FileField(write_only=True, allow_null=True, required=False)

    class Meta:
        model = UserSettings
        fields = ['general_instructions', 'terminology', 'template_name',
                  'project_instructions', 'template_content']


class AccountSerializer(ModelSerializer):
    """ Base account serializer for view/update info """

    settings = UserSettingsSerializer()

    class Meta:
        model = User
        read_only_fields = ['is_active', 'email', 'is_superuser']
        fields = ['id', 'email', 'first_name', 'last_name',
                  'is_active', 'last_login', 'created_at', 'settings']

    def update(self, instance, validated_data):
        settings_data = validated_data.pop('settings')
        settings = instance.settings

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        settings.general_instructions = settings_data.get('general_instructions',
                                                          settings.general_instructions)
        settings.terminology = settings_data.get('terminology', settings.terminology)
        settings.project_instructions = settings_data.get('project_instructions')
        template_content_file = settings_data.get('template_content')
        if template_content_file:

            if isinstance(template_content_file.file, tempfile._TemporaryFileWrapper):
                with open(template_content_file.file.name, 'rb') as f:
                    byte_content = f.read()
            else:
                byte_content = template_content_file.file.getvalue()

            self.__check_pptx(byte_content)

            settings.template_content = byte_content

            if 'template_name' not in settings_data or not validated_data.get('template_name'):
                settings_data['template_name'] = template_content_file.name

        else:
            settings.template_content = None

        settings.template_name = settings_data.get('template_name')
        settings.save()

        return instance

    def __check_pptx(self, byte_content: bytes):
        try:
            ppt_content = io.BytesIO(byte_content)
            Presentation(ppt_content)
        except Exception as e:
            logger.error('Invalid file type, error: %s', e, exc_info=True)
            raise ValidationError("Invalid file type.")


class PasswordResetConfirmSerializer(ModelSerializer):
    """Password reset confirm serializer"""

    token = CharField(max_length=100, write_only=True)
    password = CharField(write_only=True, validators=[validate_password], required=True)
    password2 = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['is_active', 'email', 'first_name', 'last_name']

    def validate(self, attrs):
        user = self.context['user']

        valid_token = expiring_token_generation.check_token(user, attrs['token'])

        if not valid_token:
            raise UserVerificationLinkInvalid('Reset password link is invalid')

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class EmailConfirmSerializer(ModelSerializer):
    """Email confirm serializer"""

    token = CharField(max_length=100, write_only=True)

    class Meta:
        model = User
        exclude = ['password']
        read_only_fields = ['is_active', 'email', 'first_name', 'last_name']

    def validate(self, attrs):
        user = self.context['user']

        valid_token = email_expiring_token_generation.check_token(user, attrs['token'])

        if not valid_token:
            raise UserVerificationLinkInvalid('Activation link is invalid')

        return attrs

    def update(self, instance, validated_data):
        instance.is_active = True
        instance.save()

        return instance


class RegistrationSerializer(ModelSerializer):
    """Registration serializer"""

    email = EmailField(validators=[UniqueValidator(queryset=User.objects.all(), lookup='iexact')])
    password = CharField(write_only=True, validators=[validate_password])
    password2 = CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['is_active']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise ValidationError('Password fields didn\'t match.')

        del attrs['password2']

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(raw_password=password)
        user.save()

        UserSettings.objects.create(user=user)

        return user
