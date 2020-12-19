import os
from environs import Env

env = Env()
# Read .env into os.environ
path = os.getcwd()
env.read_env(".env")

DEBUG = env.bool("DEBUG", True)
SECRET_KEY = env("SECRET_KEY", "ASDASD123")

SERVER = os.getenv("SERVER", default='127.0.0.1')

SERVER_NAME = os.getenv("SERVER_NAME")
SERVER_HOST = os.getenv("SERVER_HOST")

BACKEND_CORS_ORIGINS = os.getenv("BACKEND_CORS_ORIGINS")

SENTRY_DSN = env.str("SENTRY_DSN", None)

POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

CELERY_BACKEND = os.getenv("CELERY_BACKEND", "")
CELERY_BROKER = os.getenv("CELERY_BROKER", "")
CELERY_REDBEAT_REDIS_URL = os.getenv("CELERY_REDBEAT_REDIS_URL", "")

CACHE_BACKEND = os.getenv("CACHE_BACKEND", "default")
REDIS_SERVER = os.getenv("REDIS_SERVER", "")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
REDIS_DB = os.getenv("REDIS_DB", "")
REDIS_PORT = os.getenv("REDIS_PORT", "")
REDIS_CONNECT_TIMEOUT = os.getenv("REDIS_CONNECT_TIMEOUT", 5)
REDIS_SOCKET_TIMEOUT = os.getenv("SOCKET_TIMEOUT", 5)

EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', "")
EMAIL_HOST = os.getenv('EMAIL_HOST', "")
EMAIL_PORT = os.getenv('EMAIL_PORT', "")
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', "")
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD',"")

