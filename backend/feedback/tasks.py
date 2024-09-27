import logging

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from server.celery import app
from accounts.models import User


logger = logging.getLogger('accounts.task')


@app.task
def feedback_task(feedback_message: str, feedback_url: str, user_id: int):

    user = User.objects.get(id=user_id)

    mail_subject = 'New feedback received from {}'.format(user.get_full_name())

    message = render_to_string(
        template_name='feedbacks/feedback.html',
        context={
            'feedback_message': feedback_message,
            'feedback_url': feedback_url
        }
    )

    email = EmailMessage(
        mail_subject,
        message,
        to=[settings.ADMIN_EMAIL],
        from_email=settings.EMAIL_FROM
    )

    try:
        email.send()
    except Exception as e:
        logger.error('Cannot send feedback', exc_info=e)
