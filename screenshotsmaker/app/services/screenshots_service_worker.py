import logging
import time
from threading import Thread

from redis import Redis

from app.config.factories import new_redis_client
from app.config.queues import QUEUE_SCREENSHOT_REQUEST
from app.services import proc_sweeper
from app.services.screenshots_service import ScreenshotsService

logger = logging.getLogger()


def start_worker_thread() -> Thread:
    thread = Thread(target=run_worker, daemon=True)
    thread.start()
    return thread


def run_worker():
    redis_conn = None
    logger.info(f"Service worker started")
    while True:
        try:
            if not redis_conn:
                logger.info(f"Acquiring new redis connection")
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
    ret = redis_conn.blpop([QUEUE_SCREENSHOT_REQUEST], timeout=5)
    if not ret:
        return
    queue, payload = ret
    try:
        task_id = int(payload)
    except ValueError:
        raise ValueError(f"Invalid task id '{payload}' in {QUEUE_SCREENSHOT_REQUEST}")
    logger.info(f"Starting processing request for #{task_id}")
    ScreenshotsService(redis_conn=redis_conn).create_screenshots(task_id)
    logger.info(f"Finished processing request for #{task_id}")
