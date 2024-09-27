from __future__ import absolute_import
import os

from celery import Celery
from kombu import Exchange, Queue

os.environ.setdefault("FORKED_BY_MULTIPROCESSING", "1") # for windows
os.environ.setdefault(key='DJANGO_SETTINGS_MODULE', value='server.settings')

app = Celery('server')
app.config_from_object(obj='django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.task_queues = (
    Queue('openai', Exchange('openai'), routing_key='openai'),
    Queue('mail_notification', Exchange('mail_notification'), routing_key='mail_notification'),
    Queue('ppt_task_creator', Exchange('ppt_task_creator'), routing_key='ppt_task_creator'),
)

QUEUE_ROUTES = {
    'openai': {'queue': 'openai', 'routing_key': 'openai'},
    'mail_notification': {'queue': 'mail_notification', 'routing_key': 'mail_notification'},
    'ppt_task_creator': {'queue': 'ppt_task_creator', 'routing_key': 'ppt_task_creator'},
}

app.conf.task_routes = {
    'accounts.tasks.email_verification_task': QUEUE_ROUTES['mail_notification'],
    'accounts.tasks.password_reset_task': QUEUE_ROUTES['mail_notification'],
    'feedback.tasks.feedback_task': QUEUE_ROUTES['mail_notification'],
    'ppt_projects.tasks.create_slide_text_content_task': QUEUE_ROUTES['openai'],
    'ppt_projects.tasks.create_ppt_task': QUEUE_ROUTES['ppt_task_creator'],
}

app.conf.update(
    task_annotations={
        'bot.tasks.py.openai_task': {
            'rate_limit': "500/m"
        },
    },
    task_queues=app.conf.task_queues,
    task_routes=app.conf.task_routes,
)
