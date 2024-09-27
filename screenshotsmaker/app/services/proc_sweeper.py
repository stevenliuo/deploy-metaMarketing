import logging
import time
from threading import Thread

import psutil

logger = logging.getLogger("APP.process-killer")


def start_worker_thread() -> Thread:
    thread = Thread(target=run_worker, daemon=True)
    thread.start()
    return thread


def run_worker():
    while True:
        try:
            kill_old_processes(30)
        except Exception as e:
            logger.warning(f"Old processes killer worker experienced an error: {e}")
        time.sleep(10)


def kill_old_processes(age: int):
    _kill_old_excel(age)
    _kill_old_powerpoint(age)


def _kill_old_excel(age: int):
    _kill_proc("EXCEL.EXE", age)


def _kill_old_powerpoint(age: int):
    _kill_proc("POWERPNT.EXE", age)


def _kill_proc(proc_name: str, age: int):
    """ Kill process with  proc_name and running time more than age

        :param proc_name: process name, e.g. EXCEL.EXE
        :param age: required age of process in seconds
    """
    for proc in psutil.process_iter(["pid", "name", "create_time"]):
        try:
            if proc.info['name'] and proc_name == proc.info['name']:
                pid = proc.info['pid']
                name = proc.info['name']
                create_time = proc.info['create_time']
                runtime = time.time() - create_time
                if runtime > age:
                    logger.warning(f"Killing PID: {pid}, Process Name: {name}, Running Seconds: {int(runtime)}")
                    proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
