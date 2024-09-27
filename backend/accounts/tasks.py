import logging

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.conf import settings

from server.celery import app
from accounts.models import User
from accounts.tokens import email_expiring_token_generation, expiring_token_generation


logger = logging.getLogger('accounts.task')


@app.task
def email_verification_task(email: str, protocol: str):

    user = User.objects.get(email=email)

    mail_subject = 'Confirm access for {}'.format(user.get_full_name())

    message = render_to_string(
        template_name='accounts/confirm_email.html',
        context={
            'domain': settings.DOMAIN,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': email_expiring_token_generation.make_token(user),
            'protocol': protocol,
            'user': user.get_full_name()
        }
    )

    email = EmailMessage(
        mail_subject,
        message,
        to=[settings.ADMIN_EMAIL],
        from_email=settings.EMAIL_FROM
    )

    print(email.body, email.to)

    try:
        email.send()
    except Exception as e:
        logger.error('Cannot send verification email', exc_info=e)


@app.task
def password_reset_task(email: str, protocol: str):
    mail_subject = 'Reset your user password.'

    user = User.objects.get(email=email)

    message = render_to_string(
        template_name='accounts/reset_password.html',
        context={
            'domain': settings.DOMAIN,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': expiring_token_generation.make_token(user),
            'protocol': protocol
        }
    )

    email = EmailMessage(mail_subject, message, to=[email], from_email=settings.EMAIL_FROM)

    try:
        email.send()
    except Exception as e:
        logger.error('Cannot send password reset email', exc_info=e)
