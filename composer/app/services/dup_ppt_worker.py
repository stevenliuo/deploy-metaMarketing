import logging
import time
from threading import Thread

from redis import Redis

from app.config.factories import new_redis_client
from app.config.queues import QUEUE_PPT_DUP_RESPONSE
from app.services.ppt_dup_service import PptDupService

logger = logging.getLogger("app:dup-ppt-worker")


def start_worker_thread() -> Thread:
    thread = Thread(target=run_worker, daemon=True)
    thread.start()
    logger.info("PPT slides duplicator worker started")
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
    response_queue = QUEUE_PPT_DUP_RESPONSE % "composer"
    ret = redis_conn.blpop(response_queue, timeout=10)
    if not ret:
        return
    queue, payload = ret
    try:
        task_id = int(payload)
    except ValueError:
        raise ValueError(f"Invalid task id '{payload}' in {response_queue}")
    logger.info(f"Starting processing request for #{task_id} @ {queue}")
    srv = PptDupService(redis_conn=redis_conn)
    srv.receive(task_id)
    logger.info(f"Finished processing request for #{task_id} @ {queue}")

