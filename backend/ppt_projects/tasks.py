import json
import time
import logging

from celery.result import AsyncResult
from django_redis import get_redis_connection
from django.conf import settings
from django.db import transaction

from accounts.models import UserSettings
from ppt_projects.models import SlideInstructions, InputSpreadsheet, Project
from microservices_tasks.models import CreatePPTTask, CreatePPTTaskSlide
from server.celery import app
from xlsx_worker import get_workbook_sheet_data
from openAI_worker import OpenAIWorker

logger = logging.getLogger('accounts.task')


def wait_tasks(tasks_ids: list[str]):
    """Utils for wait celery tasks"""

    tasks = [AsyncResult(task_id) for task_id in tasks_ids or []]

    while tasks:
        for task in tasks:
            if task.ready():
                tasks.remove(task)
        time.sleep(0.5)


@app.task
def create_slide_text_content_task(
        user_id: int,
        spreadsheet_id: int,
        slide_id: int,
        slide_title: str,
        specific_instructions: str
) -> None:
    """ Create slide text content task using OpenAI"""

    user_settings = UserSettings.objects.get(user__id=user_id)
    spreadsheet = InputSpreadsheet.objects.filter(
        id=spreadsheet_id).select_related('input_workbook').first()

    sheet_name = spreadsheet.name
    sheet_data = get_workbook_sheet_data(spreadsheet.input_workbook.content, sheet_name)
    sheet_data = json.dumps(sheet_data)

    sys_message_prompt = "You are a model that generates text content for ppt slides."

    if user_settings.general_instructions:
        sys_message_prompt += f"\nGeneral instructions: {user_settings.general_instructions}"

    if user_settings.terminology:
        sys_message_prompt += f"\nSome terminology: {user_settings.terminology}"

    user_message_prompt = f"Generate text content for PowerPoint slide with title: {slide_title};" \
                          f" and  specific instructions: {specific_instructions}." \
                          f"\nXlsx data is represented as json: {sheet_data}." \
                          "\nReturn only text for slide content, without title, content, "\
                          "comments, symbols, etc."

    openai_worker = OpenAIWorker()

    answer = openai_worker.get_answer_from_gpt(
        user_message=user_message_prompt, sys_message=sys_message_prompt
    )

    slide = SlideInstructions.objects.get(id=slide_id)
    slide.generated_text = answer

    slide.save()

    logger.info('Text content created for slide %s', slide_id)
    logger.info('Gpt answer: %s', answer)


@app.task
def create_ppt_task(project_id: int, user_id: int) -> None:
    """ Create PPT task, when all GPT tasks are finished"""

    red = get_redis_connection("microservices")

    project = Project.objects.get(id=project_id)

    user_settings = UserSettings.objects.get(user__id=user_id)

    slides = SlideInstructions.objects.select_related(
        'input_spreadsheet').filter(project=project).all()

    tasks = []
    for slide in slides:
        task = create_slide_text_content_task.apply_async(
            kwargs={
                'user_id': user_id,
                'spreadsheet_id': slide.input_spreadsheet.id,
                'slide_id': slide.id,
                'slide_title': slide.specific_title,
                'specific_instructions': slide.specific_instructions
            }
        )
        tasks.append(task)

    wait_tasks([task.id for task in tasks])

    logger.info('GPT tasks is already finished')

    slides = SlideInstructions.objects.select_related(
        'input_spreadsheet').filter(project=project).all()

    with transaction.atomic():
        footer = project.footer
        microservice_task = CreatePPTTask.objects.create(
            name=project.title,
            title=project.title,
            subtitle=project.subtitle,
            footer=footer or user_settings.project_instructions,
            ppt_template=project.template_content or user_settings.template_content,
            extra_data=json.dumps({"project_id": project.id}),
        )

        bulk_slides = []

        for slide in slides:
            task_slide = CreatePPTTaskSlide(
                position=slide.position,
                slide_option=slide.slide_option,
                content=slide.generated_text,
                title=slide.specific_title,
                ppt_task=microservice_task
            )
            if slide.slide_option != 2:
                task_slide.spreadsheet_screenshot = slide.input_spreadsheet.screenshot

            bulk_slides.append(task_slide)

        CreatePPTTaskSlide.objects.bulk_create(bulk_slides)

    red.rpush(settings.MICROSERVICES_CREATE_PPT_TASK_QUEUE, microservice_task.id)

    project.is_generating = True
    project.save()

    logger.info('PPT task created with client_id %s', microservice_task.id)
