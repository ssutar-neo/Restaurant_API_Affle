from celery import shared_task
from django.core.management import call_command

@shared_task
def run_my_command():
    call_command('load_csv') 
