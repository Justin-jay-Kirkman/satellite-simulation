from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'satellite_project.settings')

app = Celery('satellite_project', broker=settings.CELERY_BROKER_URL)
app.conf.enable_utc = False

app.conf.update(timezone=settings.TIME_ZONE)

# Configure Celery using settings from Django settings.py.
app.config_from_object(settings, namespace='CELERY')

#Celery Beat settings

# Load tasks from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# add this to fix container issues
# app.loader.override_backends['django-db'] = 'django_celery_results.backends.database:DatabaseBackend'

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
