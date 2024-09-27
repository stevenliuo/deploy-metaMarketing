import logging
import os

from app.config import settings


def configure():
    _configure_logging()


def _configure_logging():
    if settings.LOG_DIR and settings.LOG_DIR != '-':
        from logging import handlers
        os.makedirs(settings.LOG_DIR, exist_ok=True)
        rotating_handler = handlers.RotatingFileHandler(
            os.path.join(settings.LOG_DIR, 'app.log'),
            mode='a',
            maxBytes=settings.LOG_MAX_BYTES,
            backupCount=settings.LOG_BACKUP_COUNT
        )
        logging.basicConfig(
            level=settings.LOG_LEVEL,
            format=settings.LOG_FORMAT,
            handlers=[
                rotating_handler,
                logging.StreamHandler()
            ]
        )
    else:
        logging.basicConfig(
            level=settings.LOG_LEVEL,
            format=settings.LOG_FORMAT)
