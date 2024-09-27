from app.config import configurer
from app.services import ppt_worker, screenshots_ready_worker, dup_ppt_worker

if __name__ == '__main__':
    configurer.configure()
    threads = [
        ppt_worker.start_worker_thread(),
        dup_ppt_worker.start_worker_thread(),
        screenshots_ready_worker.start_worker_thread(),
    ]

    for th in threads:
        th.join()
