import sys

from django.apps import AppConfig


class MicroservicesTasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'microservices_tasks'

    def ready(self):
        """Here we run our tasks for getting screenshots and creating PPT files on background"""

        if 'gunicorn.py' in sys.argv:
            from microservices_tasks.utils import ppt_worker, screenshot_worker

            screenshot_worker()
            ppt_worker()
