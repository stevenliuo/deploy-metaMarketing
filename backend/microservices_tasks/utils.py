import io
import json
import os.path
import time
import hashlib
import logging
from datetime import datetime

import redis
import redis_lock
from django.conf import settings
from django.db import transaction
from django.core.files.base import ContentFile
from django_redis import get_redis_connection
from django.core.files.storage import default_storage

from microservices_tasks.models import CreateScreenshotTask, CreatePPTTask
from ppt_projects.models import InputWorkbook, InputSpreadsheet, Project, SlideInstructions


logger = logging.getLogger(__name__)


def create_screenshot_task(workbook_instance: InputWorkbook) -> None:
    """Function for creating screenshot task"""

    red = get_redis_connection('microservices')

    task = CreateScreenshotTask.objects.create(
        name=workbook_instance.name,
        extra_data=json.dumps({"input_workbook_id": workbook_instance.id}),
        content_hash=hashlib.sha1(workbook_instance.content).hexdigest(),
        content=workbook_instance.content
    )

    red.lpush(settings.MICROSERVICES_CREATE_SCREENSHOT_TASK_QUEUE, task.id)


def screenshot_worker() -> None:
    """function for collecting the result from screenshot task"""

    redis_conn: redis.Redis = get_redis_connection('microservices')

    lock_time = redis_conn.ttl('lock:screenshot-worker')

    logger.info("lock_time: %s", lock_time)

    if lock_time > 0:
        time.sleep(lock_time + 1)
    else:
        time.sleep(2)

    lock = redis_lock.Lock(redis_conn, "screenshot-worker", expire=30, auto_renewal=True)

    if lock.acquire(blocking=False):
        try:
            logger.info("Start screenshot worker")
            _screenshot_worker(redis_conn)
            lock.release()
        finally:
            lock.release()
    else:
        logger.info("Screenshot worker locked")


def ppt_worker() -> None:
    """function for collecting the result from PPT task"""

    redis_conn = get_redis_connection('microservices')
    lock = redis_lock.Lock(redis_conn, "ppt-worker", expire=30, auto_renewal=True)

    lock_time = redis_conn.ttl('lock:ppt-worker')

    logger.info("lock_time: %s", lock_time)

    if lock_time > 0:
        time.sleep(lock_time + 1)
    else:
        time.sleep(2)

    if lock.acquire(blocking=False):
        try:
            logger.info("Start ppt worker")
            _ppt_worker(redis_conn)
            lock.release()
        finally:
            lock.release()
    else:
        logger.debug("PPT worker locked")


def _screenshot_worker(redis_conn: redis.Redis = None) -> None:
    red = redis_conn if redis_conn else get_redis_connection('microservices')

    while True:
        try:
            queue, payload = red.blpop(settings.MICROSERVICES_SCREENSHOT_TASK_RESULT_QUEUE)
            task_id = int(payload)

            logger.info('Got screenshot task result with id %s', task_id)

            task = CreateScreenshotTask.objects.prefetch_related('screenshots').get(id=task_id)

            if not task:
                logger.info('Screenshot task with id %s not found', task_id)
                continue

            if task.status == 'FAILED':
                extra_data = json.loads(task.extra_data)

                attempt = extra_data.get('attempt', 0)

                if attempt < 5:
                    task.status = 'PENDING'
                    extra_data.update({'attempt': attempt + 1})
                    task.extra_data = json.dumps(extra_data)
                    task.save()
                    logger.info(task.extra_data)
                    red.rpush(settings.MICROSERVICES_CREATE_SCREENSHOT_TASK_QUEUE, task.id)
                    continue

            if task.status == 'COMPLETED':

                extra_data = json.loads(task.extra_data)

                _id = extra_data['input_workbook_id']

                workbook = InputWorkbook.objects.prefetch_related('input_spreadsheets').get(id=_id)

                bulk_list = []

                for sheet in task.screenshots.all():
                    item = workbook.input_spreadsheets.get(position=sheet.position + 1)
                    item.screenshot = sheet.content
                    bulk_list.append(item)

                InputSpreadsheet.objects.bulk_update(bulk_list, ['screenshot'])

                logger.info('Update screenshots for workbook with id %s', _id)
        except Exception as e:
            logger.error('Error in screenshot worker', exc_info=e)
            time.sleep(5)


def _ppt_worker(redis_conn: redis.Redis = None) -> None:
    red = redis_conn if redis_conn else get_redis_connection('microservices')

    while True:
        try:
            queue, payload = red.blpop(settings.MICROSERVICES_PPT_TASK_RESULT_QUEUE)
            task_id = int(payload)

            logger.info('Got ppt task result with id %s', task_id)

            task = CreatePPTTask.objects.prefetch_related('ppt_task_slides').get(id=task_id)

            if not task:
                logger.info('PPT task with id %s not found', task_id)
                continue

            if task.status == 'FAILED':

                extra_data = json.loads(task.extra_data)

                attempt = extra_data.get('attempt', 0)

                if attempt < 5:
                    logger.info('PPT task with id %s failed, recreating', task_id)
                    task.status = 'PENDING'
                    extra_data.update({'attempt': attempt + 1})
                    task.extra_data = json.dumps(extra_data)
                    task.save()
                    red.rpush(settings.MICROSERVICES_CREATE_SCREENSHOT_TASK_QUEUE, task.id)
                    continue

                else:
                    project = Project.objects.prefetch_related('slide_instructions').get(id=_id)
                    project.is_generating = False
                    project.save()
                    return

            if task.status == 'COMPLETED':

                extra_data = json.loads(task.extra_data)

                _id = extra_data['project_id']

                with transaction.atomic():

                    project = Project.objects.prefetch_related('slide_instructions').get(id=_id)

                    project.ppt_content = task.created_ppt_content

                    file_name = datetime.now().strftime('%Y%m%d%H%M%S') + '-position-0.png'
                    file = io.BytesIO(task.screenshot_first_slide)

                    logger.info(f'Screenshot data size: {len(task.screenshot_first_slide)} bytes')

                    old_file_path = None
                    old_screenshot_path = None
                    if project.screenshot_first_slide:
                        old_file_path = project.screenshot_first_slide.path

                    project.screenshot_first_slide.save(file_name, ContentFile(file.getvalue()), save=True)

                    if old_file_path and os.path.isfile(old_file_path):
                        os.remove(old_file_path)

                    bulk_list = []

                    for slide in task.ppt_task_slides.all():

                        item = project.slide_instructions.get(position=slide.position)
                        file_name = datetime.now().strftime(
                            '%Y%m%d%H%M%S') + f'-position-{slide.position}.png'
                        file = io.BytesIO(slide.screenshot)

                        if item.screenshot:
                            old_screenshot_path = item.screenshot.path

                        item.screenshot.save(file_name, ContentFile(file.getvalue()))
                        bulk_list.append(item)

                        if old_screenshot_path and os.path.isfile(old_screenshot_path):
                            os.remove(old_screenshot_path)
                            old_screenshot_path = None

                    SlideInstructions.objects.bulk_update(bulk_list, ['screenshot'])
                    project.is_generating = False
                    project.save()

                    logger.info('First page screenshot is located at %s', project.screenshot_first_slide.path)
                    logger.info(os.path.isfile(project.screenshot_first_slide.path))

                logger.info('Update screenshots and ppt for project with id %s', _id)
        except Exception as e:
            logger.error('Error in ppt worker', exc_info=e)
            time.sleep(5)
