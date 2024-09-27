import json
import logging

from redis import Redis

from app.config import queues
from app.config.database import new_session
from app.config.factories import new_redis_client
from app.config.queues import QUEUE_PPT_DUP_REQUEST
from app.models.models import CreatePPTTasks, TasksStatus, DuplicatePPTSlidesTask, CreatePPTTasksSlides
from app.services.ppt_service import PptService

logger = logging.getLogger("app:ppt-dup-service")


class PptDupService:
    def __init__(self, *, redis_conn: Redis = None):
        super().__init__()
        self._redis_conn = redis_conn or new_redis_client()

    def send(self, create_ppt_tasks_id: int):
        with new_session() as session:
            t = session.query(CreatePPTTasks).filter(
                CreatePPTTasks.id == create_ppt_tasks_id,
            ).first()
            # hint the correct type
            task: CreatePPTTasks = t

            if not task or task.status != TasksStatus.PENDING:
                return

            slides_count = session.query(CreatePPTTasksSlides).filter(
                CreatePPTTasksSlides.ppt_task_id == create_ppt_tasks_id,
            ).count()
            dup_task = DuplicatePPTSlidesTask(
                client_uid="composer",
                extra_data=json.dumps({"create_ppt_tasks_id": task.id}),
                ppt_in=task.ppt_template,
                ppt_out=None,
                target_count=slides_count + 1,
                status=TasksStatus.PENDING,
                status_message="Pending",
            )
            session.add(dup_task)
            task.status_message = "Duplicating slides"
            session.commit()
            self._redis_conn.rpush(QUEUE_PPT_DUP_REQUEST, str(dup_task.id))

    def receive(self, dup_task_id: int):
        notify = False
        with new_session() as session:
            t = session.query(DuplicatePPTSlidesTask).filter(
                DuplicatePPTSlidesTask.id == dup_task_id,
            ).first()
            dup_task: DuplicatePPTSlidesTask = t

            if not dup_task:
                return

            extra_data = json.loads(dup_task.extra_data)
            create_ppt_tasks_id = extra_data["create_ppt_tasks_id"]
            t = session.query(CreatePPTTasks).filter(
                CreatePPTTasks.id == create_ppt_tasks_id,
            ).first()
            create_ppt_task: CreatePPTTasks = t
            client_uid = create_ppt_task.client_uid

            if not create_ppt_task:
                return

            if dup_task.status != TasksStatus.COMPLETED:
                create_ppt_task.status = TasksStatus.FAILED
                create_ppt_task.status_message = "Failed to duplicate slides"
                notify = True
            else:
                create_ppt_task.status_message = "Slides duplicated"
                create_ppt_task.created_ppt_content = dup_task.ppt_out

            session.commit()
            # detach create_ppt_task from session
            session.expunge(create_ppt_task)

        if notify:
            logger.error(f"Failed to duplicate slides for {create_ppt_tasks_id}")
            self._redis_conn.rpush(queues.QUEUE_PPT_RESPONSE % client_uid, str(create_ppt_tasks_id))
        else:
            logger.info(f"Duplicated slides for {create_ppt_tasks_id}, creating PPT")
            PptService(redis_conn=self._redis_conn).create_ppt(create_ppt_tasks_id)
