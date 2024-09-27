import logging
import time
from threading import Thread

from redis import Redis

from app.config.factories import new_redis_client
from app.config.queues import QUEUE_PPT_REQUEST, QUEUE_PPT_DUP_REQUEST
from app.services.ppt_dup_service import PptDupService
from app.services.ppt_service import PptService

logger = logging.getLogger("app:ppt-worker")


def start_worker_thread() -> Thread:
    thread = Thread(target=run_worker, daemon=True)
    thread.start()
    logger.info("PPT worker started")
    return thread


def run_worker():
    redis_conn = None
    while True:
        try:
            if not redis_conn:
                redis_conn = new_redis_client()
            _handle_request(redis_conn)
        except Exception as e:
            logger.exception(f"Service worker failure: {e}")
            try:
                if redis_conn:
                    redis_conn.close()
            except Exception as e:
                logger.warning(f"Failed to close redis connection: {e}")
            redis_conn = None
            time.sleep(10)


def _handle_request(redis_conn: Redis):
    ret = redis_conn.blpop([QUEUE_PPT_REQUEST], timeout=10)
    if not ret:
        return
    queue, payload = ret
    try:
        task_id = int(payload)
    except ValueError:
        raise ValueError(f"Invalid task id '{payload}' in {QUEUE_PPT_REQUEST}")
    logger.info(f"Starting processing request for #{task_id} @ {queue}")
    srv = PptDupService(redis_conn=redis_conn)
    srv.send(task_id)
    logger.info(f"Sent to slides dup for #{task_id} @ {QUEUE_PPT_REQUEST}")
