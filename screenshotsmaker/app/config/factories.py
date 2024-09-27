from threading import Lock

import redis
from redis import Redis

from app.config import settings
from app.screenshots.excel import ExcelScreenshotMaker
from app.screenshots.powerpoint import PowerPointScreenshotMaker


def new_excel_screenshot_maker() -> ExcelScreenshotMaker:
    """ Create a new instance of ExcelScreenshotMaker """
    box = (settings.SS_EXCEL_CROPBOX_X, settings.SS_EXCEL_CROPBOX_Y,
           settings.SS_EXCEL_CROPBOX_WIDTH, settings.SS_EXCEL_CROPBOX_HEIGHT)
    return ExcelScreenshotMaker(box=box)


def new_power_point_screenshot_maker() -> PowerPointScreenshotMaker:
    """ Create a new instance of PowerPointScreenshotMaker """
    box = (settings.SS_POWERPOINT_CROPBOX_X, settings.SS_POWERPOINT_CROPBOX_Y,
           settings.SS_POWERPOINT_CROPBOX_WIDTH, settings.SS_POWERPOINT_CROPBOX_HEIGHT)
    return PowerPointScreenshotMaker(box=box)


def new_redis_client() -> Redis:
    """ Create a new instance of Redis Client """
    return redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
        decode_responses=True,
        socket_connect_timeout=10,
        socket_timeout=10,
    )
