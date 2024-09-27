import logging

from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from accounts.tasks import email_verification_task, password_reset_task
from accounts.models import User
from accounts import serializers


logger = logging.getLogger('accounts')


class AccountInfoAPIView(APIView):
    """ Account info view """

    serializer_class = serializers.AccountSerializer
    queryset = User.objects.all()

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RegistrationAPIView(CreateAPIView):
    """ Account registration view """

    serializer_class = serializers.RegistrationSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        protocol = 'https' if self.request.is_secure() else 'http'
        email_verification_task.apply_async(args=[user.email, protocol])


class EmailConfirmAPIView(APIView):
    """Email confirmation view"""

    serializer_class = serializers.EmailConfirmSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def post(self, request, pk):

        try:
            user = self.queryset.get(id=pk)
        except User.DoesNotExist:
            raise APIException("User doesn't exist.")

        context = {'user': user}

        serializer = self.serializer_class(user, data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'detail': 'Email confirmation was successful'})


class PasswordResetAPIView(APIView):
    """ Password reset view """

    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'detail': 'Field email required'})

        try:
            self.queryset.get(email=email)
        except User.DoesNotExist:
            raise APIException('User does\'t exist.')

        protocol = 'https' if self.request.is_secure() else 'http'

        password_reset_task.apply_async(args=[email, protocol])

        return Response({'detail': 'Password reset confirmation sent to email'})


class PasswordResetConfirmAPIView(APIView):
    """ Password reset confirmation view """

    serializer_class = serializers.PasswordResetConfirmSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def post(self, request, pk):

        try:
            user = self.queryset.get(id=pk)
        except User.DoesNotExist:
            raise APIException("User doesn't exist.")

        context = {'user': user}

        serializer = self.serializer_class(user, data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'detail': 'Password successfully reset'})
