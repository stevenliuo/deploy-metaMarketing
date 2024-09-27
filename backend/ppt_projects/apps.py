from django.apps import AppConfig


class PptProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ppt_projects'

    def ready(self):
        import ppt_projects.signals
