import logging
import time
from threading import Thread

from redis import Redis

from app.config.factories import new_redis_client
from app.config.queues import QUEUE_SCREENSHOT_RESPONSE
from app.services.screenshots_service import ScreenshotsService

logger = logging.getLogger("app:screenshots-ready-worker")


def start_worker_thread() -> Thread:
    thread = Thread(target=run_worker, daemon=True)
    thread.start()
    logger.info("Screenshots ready worker started")
    return thread


def run_worker():
    redis_conn = None
    while True:
        try:
            if not redis_conn:
                redis_conn = new_redis_client()
            _handle_response(redis_conn)
        except Exception as e:
            logger.exception(f"Service worker failure: {e}")
            try:
                if redis_conn:
                    redis_conn.close()
            except Exception as e:
                logger.warning(f"Failed to close redis connection: {e}")
            redis_conn = None
            time.sleep(10)


def _handle_response(redis_conn: Redis):
    ret = redis_conn.blpop([QUEUE_SCREENSHOT_RESPONSE % "composer"], timeout=10)
    if not ret:
        return
    queue, payload = ret
    try:
        task_id = int(payload)
    except ValueError:
        raise ValueError(f"Invalid task id '{payload}'")
    logger.info(f"Starting processing response of #{task_id}")
    srv = ScreenshotsService(redis_conn=redis_conn)
    srv.process_response(task_id)
    logger.info(f"Finished processing response of #{task_id}")
