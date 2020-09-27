import os

from celery import Celery, platforms
from tasks import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tantan.settings')

celery_app = Celery('tasks')
celery_app.config_from_object(config)
celery_app.autodiscover_tasks()

# 运行云服务器的root用户运行
platforms.C_FORCE_ROOT = True
