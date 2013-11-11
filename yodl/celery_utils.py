"""
See this:
https://hynek.me/articles/using-celery-with-pyramid/
"""
from celery import Celery


celery_config = lambda: None

celery_config.CELERY_RESULT_DBURI = "sqlite:///file.db"
celery_config.CELERY_RESULT_BACKEND = "database"
celery_config.BROKER_URL = ""
celery_config.CELERYD_TASK_TIME_LIMIT= 60

celery = Celery()
celery.config_from_object(celery_config)


# Optional configuration, see the application user guide.
celery.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    celery.start()
