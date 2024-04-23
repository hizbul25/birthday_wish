from .base import *

DEBUG = True

HOST = "http://localhost:8000"

SECRET_KEY = "secret"

STATIC_ROOT = base_dir_join("staticfiles")
STATIC_URL = "/static/"


STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Celery
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
