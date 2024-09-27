import redis
from redis import Redis

from app.config import settings
from app.services.presentation_composer import PresentationComposer


def new_redis_client() -> Redis:
    """ Create a new instance of Redis Client """
    return redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
        decode_responses=True,
        socket_keepalive=True,
    )


def new_presentation_composer() -> PresentationComposer:
    """Create a new instance of PresentationComposer"""
    return PresentationComposer()
