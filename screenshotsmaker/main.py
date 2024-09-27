from app.config import configurer, queues
from app.config.factories import new_redis_client
from app.services import screenshots_service_worker, proc_sweeper

if __name__ == "__main__":
    configurer.configure_all()
    rc = new_redis_client()
    threads = []

    th = screenshots_service_worker.start_worker_thread()
    threads.append(th)

    th = proc_sweeper.start_worker_thread()
    threads.append(th)

    for th in threads:
        th.join()
