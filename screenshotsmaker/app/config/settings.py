import os
from collections import ChainMap

from decouple import Config, RepositoryEnv, AutoConfig, strtobool

env_file = os.environ.get("ENV_FILE")
if env_file:
    if not os.path.isfile(env_file):
        raise FileNotFoundError(env_file)
    config = Config(RepositoryEnv(env_file))
else:
    config = AutoConfig()

# Logging config
LOG_FILE = config("LOG_FILE", default="app.log")
LOG_FILE_MAX_BYTES = config("LOG_FILE_MAX_BYTES", default=1024*1024, cast=int)
LOG_FILE_BACKUP_COUNT = config("LOG_FILE_BACKUP_COUNT", default=10, cast=int)

# Database connection
DATABASE_DRIVER = config("DATABASE_DRIVER", default="postgresql")
DATABASE_HOST = config("DATABASE_HOST", default="localhost")
DATABASE_PORT = config("DATABASE_PORT", cast=int, default=5432)
DATABASE_NAME = config("DATABASE_NAME", default="webapp")
DATABASE_USER = config("DATABASE_USER", default="webapp")
DATABASE_PASSWORD = config("DATABASE_PASSWORD")
DATABASE_POOL_SIZE = config("DATABASE_POOL_SIZE", cast=int, default=2)
DATABASE_MAX_OVERFLOW = config("DATABASE_MAX_OVERFLOW", cast=lambda v: int(v) if v is not None else None,
                               default=None)
DATABASE_ECHO = config("DATABASE_ECHO", cast=strtobool, default=False)


# Redis Connection
REDIS_HOST = config("REDIS_HOST", default="localhost")
REDIS_PORT = config("REDIS_PORT", default=6379, cast=int)
REDIS_DB = config("REDIS_DB", default=0, cast=int)
REDIS_PASSWORD = config("REDIS_PASSWORD", default=None)

# Excel Screenshot Maker config
SS_EXCEL_CROPBOX_X = config("SS_EXCEL_CROPBOX_X", default=0, cast=int)
SS_EXCEL_CROPBOX_Y = config("SS_EXCEL_CROPBOX_Y", default=0, cast=int)
SS_EXCEL_CROPBOX_HEIGHT = config("SS_EXCEL_CROPBOX_HEIGHT", default=768, cast=int)
SS_EXCEL_CROPBOX_WIDTH = config("SS_EXCEL_CROPBOX_WIDTH", default=1024, cast=int)

# Presentation Screenshot Maker config
SS_POWERPOINT_CROPBOX_X = config("SS_POWERPOINT_CROPBOX_X", default=0, cast=int)
SS_POWERPOINT_CROPBOX_Y = config("SS_POWERPOINT_CROPBOX_Y", default=305, cast=int)
SS_POWERPOINT_CROPBOX_HEIGHT = config("SS_POWERPOINT_CROPBOX_HEIGHT", default=768, cast=int)
SS_POWERPOINT_CROPBOX_WIDTH = config("SS_POWERPOINT_CROPBOX_WIDTH", default=1024, cast=int)
