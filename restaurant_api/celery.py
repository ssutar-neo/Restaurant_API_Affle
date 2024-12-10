from __future__ import absolute_import, unicode_literals
from celery import Celery
import os 
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_api.settings')

app = Celery('restaurant_api')

app.config_from_object('django.conf:settings',namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'load_csv_file_to_db': {
        'task': 'delivery.tasks.run_my_command',
        'schedule': crontab(minute=0, hour='*/6'),  # Every minute
    }

}