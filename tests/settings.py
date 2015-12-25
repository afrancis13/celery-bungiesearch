import logging
import os
import sys

from celery import Celery
from kombu import Exchange, Queue

app = Celery('celery_bungiesearch')
app.config_from_object('django.conf:settings')

logging.getLogger('elasticsearch').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)

SECRET_KEY = 'bungiesearching'
INSTALLED_APPS = (
    'bungiesearch',
    'celery_bungiesearch',
    'core',
    'djcelery'
)
ROOT_URLCONF = 'urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_TZ = True
DEBUG = False
MIDDLEWARE_CLASSES = ()
DEFAULT_INDEX_TABLESPACE = ''

BUNGIESEARCH = {
    'URLS': [os.getenv('ELASTIC_SEARCH_URL', 'http://127.0.0.1:9200')],
    'INDICES': {'celery_bungiesearch_demo': 'core.indices'},
    'SIGNALS': {
        'SIGNAL_CLASS': 'celery_bungiesearch.signals.CelerySignalProcessor',
        'BUFFER_SIZE': 1
    },
    'TIMEOUT': 5,
    'ES_SETTINGS': {'http_auth': os.getenv('ELASTIC_SEARCH_AUTH')}
}

CELERY_ALWAYS_EAGER = True
CELERY_IGNORE_RESULT = True
CELERYD_LOG_LEVEL = 'ERROR'
CELERY_DEFAULT_QUEUE = 'celery-bungiesearch'
CELERY_BUNGIESEARCH_QUEUE = Queue('default', Exchange('default'), routing_key='default')
CELERY_BUNGIESEARCH_CUSTOM_TASK = 'tests.core.custom_task.CustomTask'
