import os
import dotenv

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

REDIS_DB_HOST = os.getenv('REDIS_HOST', "broker")

BASE_REDIS_URL = os.environ.get('REDIS_URL', f'redis://{REDIS_DB_HOST}:6379/0')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.broker_url = BASE_REDIS_URL

app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'

app.conf.beat_schedule = {
    'clean-db-every-24-hours': {
        'task': 'main.tasks.db_clean_up',
        'schedule': 60 * 60 * 24,  # 24 hours
    },
    'clean-links-every-2-minutes': {
        'task': 'main.tasks.delete_expired_share_links',
        'schedule': 120,  # 2 minutes
    },
}
