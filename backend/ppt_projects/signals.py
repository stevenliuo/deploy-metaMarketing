import os

from django.db.models.signals import post_delete
from django.dispatch import receiver

from ppt_projects.models import SlideInstructions, Project


@receiver(post_delete, sender=SlideInstructions)
def delete_file_on_delete(sender, instance, **kwargs):
    """Remove file from local storage when SlideInstruction instance is deleted"""

    if instance.screenshot:
        if os.path.isfile(instance.screenshot.path):
            os.remove(instance.screenshot.path)


@receiver(post_delete, sender=Project)
def delete_file_on_delete(sender, instance, **kwargs):
    """ Remove file from local storage when Project instance is deleted"""

    if instance.screenshot_first_slide:
        if os.path.isfile(instance.screenshot_first_slide.path):
            os.remove(instance.screenshot_first_slide.path)
