import json
import logging
from hashlib import md5

from redis import Redis

from app.config import queues
from app.config.database import new_session
from app.models.models import CreateScreenshotTasks, TasksStatus, CreateScreenshotTasksScreenshots, CreatePPTTasks, \
    CreatePPTTasksSlides


logger = logging.getLogger(__name__)


class ScreenshotsServiceError(Exception):
    pass


class ScreenshotsService:
    def __init__(self, redis_conn: Redis):
        self.redis_conn = redis_conn

    def request_screenshot(self, task_id: int, pptx_content: bytes):
        with new_session() as session:
            ss_task = CreateScreenshotTasks(
                client_uid="composer",
                name="composer.pptx",
                extra_data=json.dumps({"task_id": task_id}),
                content_hash=md5(pptx_content).hexdigest(),
                status=TasksStatus.PENDING,
                status_message="Submitted",
                content=pptx_content,
            )
            session.add(ss_task)
            session.flush()
            session.refresh(ss_task)
            ss_task_id = ss_task.id
            session.commit()

        self.redis_conn.rpush(queues.QUEUE_SCREENSHOT_REQUEST, str(ss_task_id))
        logger.info(f"Requesting screenshots for {task_id} at #{ss_task_id}")

    def process_response(self, screenshots_task_id: int):
        with new_session() as session:
            ss_task = session.query(CreateScreenshotTasks).filter(
                CreateScreenshotTasks.id == screenshots_task_id
            ).first()
            ss_task: CreateScreenshotTasks = ss_task

            if not ss_task:
                logger.error(f"Screenshot task {screenshots_task_id} not found")
                return

            task = session.query(CreatePPTTasks).filter(
                CreatePPTTasks.id == self._get_task_id(ss_task)
            ).first()
            task: CreatePPTTasks = task

            if not task:
                logger.error(f"PPT task {self._get_task_id(ss_task)} not found")
                return

            if ss_task.status == TasksStatus.PENDING:
                self._set_status_if_pending(task.id, TasksStatus.FAILED, "Screenshot task has invalid status")
                self._notify_task_is_done(task)
                return
            if ss_task.status == TasksStatus.FAILED:
                self._set_status_if_pending(task.id, TasksStatus.FAILED, "Failed to create presentation screenshots")
                self._notify_task_is_done(task)
                return

            task_id = self._get_task_id(ss_task)
            slides = session.query(CreatePPTTasksSlides).filter(CreatePPTTasksSlides.ppt_task_id == task_id).all()
            slides: [CreatePPTTasksSlides] = list(slides)
            # Set the main slide screenshot
            screenshot = session.query(CreateScreenshotTasksScreenshots).filter(
                CreateScreenshotTasksScreenshots.screenshot_task_id == screenshots_task_id,
                CreateScreenshotTasksScreenshots.position == 0
            ).first()
            if screenshot:
                task.screenshot_first_slide = screenshot.content

            # Set the rest of the slides screenshots
            for slide in slides:
                screenshot = session.query(CreateScreenshotTasksScreenshots).filter(
                    CreateScreenshotTasksScreenshots.screenshot_task_id == screenshots_task_id,
                    CreateScreenshotTasksScreenshots.position == slide.position
                ).first()
                if screenshot:
                    slide.screenshot = screenshot.content

            session.flush()
            session.expunge(task)
            session.commit()
        self._set_status_if_pending(task.id, TasksStatus.COMPLETED, "Screenshots added")
        self._notify_task_is_done(task)

    def _set_status_if_pending(self, task_id: int, status: TasksStatus, message: str):
        with new_session() as session:
            t = session.query(CreatePPTTasks).filter(
                CreatePPTTasks.id == task_id,
                CreatePPTTasks.status == TasksStatus.PENDING
            ).first()
            # hint the correct type
            ss_task: CreatePPTTasks = t
            if ss_task:
                ss_task.status = status
                ss_task.status_message = message
            session.commit()

    def _notify_task_is_done(self, task: CreatePPTTasks):
        logger.info(f"Screenshot task for {task.id} notified via queue {queues.QUEUE_PPT_RESPONSE % task.client_uid}")
        self.redis_conn.rpush(queues.QUEUE_PPT_RESPONSE % task.client_uid, str(task.id))

    def _get_task_id(self, ss_task: CreateScreenshotTasks) -> int:
        return json.loads(ss_task.extra_data)["task_id"]
