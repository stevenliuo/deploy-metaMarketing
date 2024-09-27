
import logging
import sys
from logging.handlers import RotatingFileHandler

from app.config import settings


def configure_all():
    configure_logging()


def configure_logging():
    handlers = [
        logging.StreamHandler(stream=sys.stdout)
    ]
    if settings.LOG_FILE:
        handlers.append(RotatingFileHandler(settings.LOG_FILE,
                                            maxBytes=settings.LOG_FILE_MAX_BYTES,
                                            backupCount=settings.LOG_FILE_BACKUP_COUNT))

    logging.basicConfig(
        handlers=handlers,
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S')
