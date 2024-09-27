import logging
import tempfile
from pathlib import Path

from redis import Redis

from app.config import queues
from app.config.database import new_session
from app.config.factories import new_redis_client
from app.database.models import DuplicatePPTSlidesTask, TasksStatus
from app.screenshots.powerpoint import SlidesCopier


logger = logging.getLogger(__name__)

class DupSlidesService:

    def __init__(self, *, redis_conn: Redis = None):
        super().__init__()
        self._redis_conn = redis_conn or new_redis_client()

    def dup(self, dup_task_id: int):
        with new_session() as session:
            t = session.query(DuplicatePPTSlidesTask).filter(
                DuplicatePPTSlidesTask.id == dup_task_id,
            ).first()
            # hint the correct type
            task: DuplicatePPTSlidesTask = t

            if not task:
                return

            if task.status != TasksStatus.PENDING:
                self._notify_task_is_done(task)
                return

            source_ppt = None
            target_path = None

            try:
                source_ppt = Path(tempfile.mktemp(suffix='.pptx'))
                source_ppt.write_bytes(task.ppt_in)
                target_path = Path(tempfile.mktemp(suffix='.pptx'))

                SlidesCopier().duplicate_slides(source_ppt, target_path, task.target_count)
                task.ppt_out = target_path.read_bytes()
                task.status = TasksStatus.COMPLETED
                task.status_message = "OK"
            except Exception as e :
                task.status = TasksStatus.FAILED
                task.status_message = str(e)
                logger.exception("Failed to dup slides")
            finally:
                try:
                    if source_ppt:
                        source_ppt.unlink(missing_ok=True)
                except IOError:
                    pass

                try:
                    if target_path:
                        target_path.unlink(missing_ok=True)
                except IOError:
                    pass
            session.commit()
            self._notify_task_is_done(task)

    def _notify_task_is_done(self, task: DuplicatePPTSlidesTask):
        self._redis_conn.rpush(queues.QUEUE_PPT_DUP_RESPONSE %  task.client_uid, task.id)

