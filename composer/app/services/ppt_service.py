import logging

import magic
from redis import Redis

from app.config import queues
from app.config.database import new_session
from app.config.factories import new_redis_client
from app.models.models import TasksStatus, CreatePPTTasks, CreatePPTTasksSlides
from app.services.presentation_composer import PresentationComposer, SlideData
from app.services.screenshots_service import ScreenshotsService

logger = logging.getLogger("app:ppt-service")


class PptService:
    def __init__(self, *, redis_conn: Redis = None):
        super().__init__()
        self._redis_conn = redis_conn or new_redis_client()

    def create_ppt(self, task_id: int):
        try:
            self._create_ppt(task_id)
        except Exception as e:
            logger.exception(f"Failed to create presentation for {task_id}")
            self._set_status_if_pending(task_id, TasksStatus.FAILED, f"Error: {e}")

    def _create_ppt(self, task_id: int):
        with new_session() as session:
            t = session.query(CreatePPTTasks).filter(
                CreatePPTTasks.id == task_id,
            ).first()
            # hint the correct type
            task: CreatePPTTasks = t

            if not task:
                return

            if task.status != TasksStatus.PENDING:
                self._notify_task_is_done(task)
                return

            slides = session.query(CreatePPTTasksSlides).filter(
                CreatePPTTasksSlides.ppt_task_id == task_id,
            ).all()
            slides: [CreatePPTTasksSlides] = list(slides)

            if not slides:
                self._set_status_if_pending(task_id, TasksStatus.FAILED, "No slides")
                self._notify_task_is_done(task)
                return

            if not task.ppt_template:
                self._set_status_if_pending(task_id, TasksStatus.FAILED, "No template")
                self._notify_task_is_done(task)
                return

        if self._is_filetype_pptx(task):
            self._process_pptx(task, slides)
        elif self._is_filetype_ppt(task):
            self._set_status_if_pending(task_id, TasksStatus.FAILED, "Old PPT format is not supported")
        else:
            self._set_status_if_pending(task_id, TasksStatus.FAILED, "Unknown file type")

    def _process_pptx(self, task: CreatePPTTasks, slides: list[CreatePPTTasksSlides]):
        composer = PresentationComposer()
        slide_data = [
            SlideData(content=slide.content, image=slide.spreadsheet_screenshot, title=slide.title, option=slide.slide_option)
            for slide in slides]
        presentation = composer.compose(task.created_ppt_content, task.title, task.subtitle, task.footer, slide_data)
        task_id = None
        with new_session() as session:
            t = session.query(CreatePPTTasks).filter(CreatePPTTasks.id == task.id).first()
            if t:
                # hint the correct type
                t: CreatePPTTasks = t
                t.created_ppt_content = presentation
                t.status_message = "Presentation created"
                task_id = t.id
            session.commit()

        if task_id:
            self._request_screenshots(task_id, presentation)

    def _is_filetype_pptx(self, task: CreatePPTTasks):
        ppt_template = task.ppt_template
        return b'PK' == ppt_template[:2]

    def _is_filetype_ppt(self, task: CreatePPTTasks):
        ppt_template = task.ppt_template
        mime = magic.from_buffer(ppt_template, mime=True)
        return mime == "application/vnd.ms-powerpoint"

    def _notify_task_is_done(self, task: CreatePPTTasks):
        self._redis_conn.rpush(queues.QUEUE_PPT_RESPONSE % task.client_uid, str(task.id))

    def _set_status_if_pending(self, task_id: int, status: TasksStatus, message: str):
        with new_session() as session:
            t = session.query(CreatePPTTasks).filter(
                CreatePPTTasks.id == task_id,
                CreatePPTTasks.status == TasksStatus.PENDING
            ).first()
            # hint the correct type
            task: CreatePPTTasks = t
            if task:
                task.status = status
                task.status_message = message
            session.commit()

    def _request_screenshots(self, task_id: int, presentation: bytes):
        ScreenshotsService(redis_conn=self._redis_conn).request_screenshot(task_id, presentation)
