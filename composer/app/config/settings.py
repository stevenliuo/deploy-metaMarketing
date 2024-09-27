import os
from collections import ChainMap

from decouple import Config, RepositoryEnv, strtobool, RepositoryEmpty

ENV_FILE = os.environ.get("ENV_FILE", ".env")
boot_config = Config(RepositoryEnv(ENV_FILE)) if os.path.exists(ENV_FILE) else Config(RepositoryEmpty())
PROFILE = boot_config("PROFILE", default=None)

if not PROFILE:
    print("PROFILE variable is not set, please set it to a valid profile:\n"
          " - dev (local development)\n"
          " - prod (production)\n"
          "\n"
          "Custom profiles can be created as needed. You can set the\n"
          "PROFILE environment variable in the shell or in the .env file.\n"
          "\n"
          "File named env_{PROFILE}.custom will be loaded if it exists. Convenient for\n"
          "switching between profiles. Not tracked by version control.\n"
          "\n"
          "File named env_{PROFILE}.defaults will be loaded if it exists. Stores default\n"
          "values for the profile.\n"
          "\n"
          "Priorities:\n"
          " - shell variable\n"
          " - .env or $ENV_FILE file\n"
          " - env_{PROFILE}.custom file\n"
          " - env_{PROFILE}.defaults file\n"
          "-  settings.py defaults\n"
          "\n"
          "You can redefine the ENV_FILE environment variable to load a different file than .env.\n")
    exit(1)

ENV_FILES = [
    ENV_FILE,
    f"env_{PROFILE}.custom",
    f"env_{PROFILE}.defaults"
]

repositories = [RepositoryEnv(f) for f in ENV_FILES if os.path.exists(f)]
config = Config(ChainMap(*repositories))

# Logging configuration
LOG_DIR = config("LOG_DIR", default="data/logs")
LOG_LEVEL = config("LOG_LEVEL", default="INFO")
LOG_FORMAT = config("LOG_FORMAT", default="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOG_MAX_BYTES = config("LOG_MAX_BYTES", cast=int, default=100 * 1024 * 1024)
LOG_BACKUP_COUNT = config("LOG_BACKUP_COUNT", cast=int, default=5)

# Redis settings
REDIS_HOST = config("REDIS_HOST", default="localhost")
REDIS_PORT = config("REDIS_PORT", cast=int, default=6379)
REDIS_DB = config("REDIS_DB", cast=int, default=0)
REDIS_PASSWORD = config("REDIS_PASSWORD", default=None)

# Database settings
DATABASE_DRIVER = config("DATABASE_DRIVER", default="postgresql")
DATABASE_HOST = config("DATABASE_HOST", default="localhost")
DATABASE_PORT = config("DATABASE_PORT", cast=int, default=5432)
DATABASE_NAME = config("DATABASE_NAME", default="webapp")
DATABASE_USER = config("DATABASE_USER", default="webapp")
DATABASE_PASSWORD = config("DATABASE_PASSWORD")
DATABASE_POOL_SIZE = config("DATABASE_POOL_SIZE", cast=int, default=2)
DATABASE_MAX_OVERFLOW = config("DATABASE_MAX_OVERFLOW", cast=lambda v: int(v) if v is not None else None, default=5)
DATABASE_ECHO = config("DATABASE_ECHO", cast=strtobool, default=False)



