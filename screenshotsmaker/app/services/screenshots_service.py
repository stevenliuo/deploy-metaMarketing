import logging
import tempfile
from pathlib import Path

from redis import Redis
from sqlalchemy import text, bindparam

from app.config import queues
from app.config.database import new_session
from app.config.factories import new_redis_client, new_excel_screenshot_maker, new_power_point_screenshot_maker
from app.database.models import CreateScreenshotTasksScreenshots, CreateScreenshotTasks, CreateScreenshotTasksStatus

logger = logging.getLogger(__name__)


class ScreenshotsService:

    def __init__(self, *, redis_conn: Redis = None):
        super().__init__()
        self._redis_conn = redis_conn or new_redis_client()

    def create_screenshots(self, task_id: int):
        with new_session() as session:
            t = session.query(CreateScreenshotTasks).filter(
                CreateScreenshotTasks.id == task_id,
            ).first()
            # hint the correct type
            task: CreateScreenshotTasks = t

        if not task:
            return

        try:
            self._create_screenshots(task)
        except Exception as e:
            logger.exception(f"Failed to create screenshot for {task_id}")
            self._set_status_if_pending(task_id, CreateScreenshotTasksStatus.FAILED, f"Error: {e}")
            self._notify_task_is_done(task)

    def _create_screenshots(self, task: CreateScreenshotTasks):
        if task.status != CreateScreenshotTasksStatus.PENDING:
            self._notify_task_is_done(task)
            return

        if self._try_already_completed(task.id):
            self._notify_task_is_done(task)
            return

        if self._is_excel(task):
            self._process_excel(task)
        elif self._is_powerpoint(task):
            self._process_powerpoint(task)
        else:
            self._set_status_if_pending(task.id, CreateScreenshotTasksStatus.FAILED, "Unknown file type")
        self._notify_task_is_done(task)

    def _is_excel(self, task: CreateScreenshotTasks) -> bool:
        ext = Path(task.name or "").suffix.upper()
        return ext in (".XLSX", ".XLS")

    def _is_powerpoint(self, task: CreateScreenshotTasks) -> bool:
        ext = Path(task.name or "").suffix.upper()
        return ext in (".PPTX", ".PPT", ".POTX", ".POT")

    def _notify_task_is_done(self, task: CreateScreenshotTasks):
        self._redis_conn.rpush(queues.QUEUE_SCREENSHOT_RESPONSE % task.client_uid, str(task.id))

    def _set_status_if_pending(self, task_id: int, status: CreateScreenshotTasksStatus, message: str):
        with new_session() as session:
            t = session.query(CreateScreenshotTasks).filter(
                CreateScreenshotTasks.id == task_id,
                CreateScreenshotTasks.status == CreateScreenshotTasksStatus.PENDING
            ).first()
            # hint the correct type
            task: CreateScreenshotTasks = t
            if task:
                task.status = status
                task.status_message = message
            session.commit()

    def _try_already_completed(self, task_id: int) -> bool:
        """ Search for existing tasks and check is this task already completed previously.

            Copy results from previously completed task with the same payload.

            :return: True if already completed, False otherwise
        """

        with new_session() as session:
            t = session.query(CreateScreenshotTasks).filter(CreateScreenshotTasks.id == task_id).first()
            # fix type hint
            task: CreateScreenshotTasks = t
            if not task:
                return False

            stmt = text("""
                SELECT prev.id
                    FROM create_screenshot_tasks curr
                        INNER JOIN create_screenshot_tasks prev ON curr.content_hash = prev.content_hash
                    WHERE
                        curr.id = :curr_id
                        AND curr.id <> prev.id
                        AND curr.content = prev.content
                        AND prev.status = 'COMPLETED'
                    ORDER BY prev.updated_at DESC
                    LIMIT 1
            """)
            prev_task_id = session.execute(stmt, params={"curr_id": task_id}).scalar_one_or_none()
            if prev_task_id is None:
                return False

            # copy result
            screenshots = session.query(CreateScreenshotTasksScreenshots).filter(
                CreateScreenshotTasksScreenshots.screenshot_task_id == prev_task_id
            ).all()

            for s in screenshots:
                # fix type hint
                prev_screenshot: CreateScreenshotTasksScreenshots = s
                screenshot = CreateScreenshotTasksScreenshots(
                    position=prev_screenshot.position,
                    content=prev_screenshot.content,
                    screenshot_task_id=task_id,
                )
                session.add(screenshot)
            task.status = CreateScreenshotTasksStatus.COMPLETED
            task.status_message = f"OK. Copied from {prev_task_id}"
            session.commit()

            return True

    def _process_excel(self, task: CreateScreenshotTasks):
        maker = new_excel_screenshot_maker()
        suffix = Path(task.name).suffix
        filename = tempfile.mktemp(suffix=suffix, prefix="screenshots_")
        file = Path(filename)
        try:
            file.write_bytes(task.content)
            screenshots = maker.make_sheet_screenshots(file)
            self._write_screenshots(task.id, screenshots)
        finally:
            try:
                file.unlink(missing_ok=True)
            except IOError:
                pass

    def _process_powerpoint(self, task: CreateScreenshotTasks):
        maker = new_power_point_screenshot_maker()
        suffix = Path(task.name).suffix
        filename = tempfile.mktemp(suffix=suffix, prefix="screenshots_")
        file = Path(filename)
        try:
            file.write_bytes(task.content)
            screenshots = maker.make_slides_screenshots(file)
            self._write_screenshots(task.id, screenshots)
        finally:
            try:
                file.unlink(missing_ok=True)
            except IOError:
                pass

    def _write_screenshots(self, task_id: int, screenshots: list[bytes]):
        with new_session() as session:
            t = session.query(CreateScreenshotTasks).filter(
                CreateScreenshotTasks.id == task_id,
                CreateScreenshotTasks.status == CreateScreenshotTasksStatus.PENDING
            ).first()
            # fix type hint
            up_task: CreateScreenshotTasks = t
            if up_task:
                for position, content in enumerate(screenshots):
                    screenshot = CreateScreenshotTasksScreenshots(
                        position=position,
                        content=content,
                        screenshot_task_id=up_task.id,
                    )
                    session.add(screenshot)
                up_task.status = CreateScreenshotTasksStatus.COMPLETED
                up_task.status_message = 'OK'

            session.commit()
