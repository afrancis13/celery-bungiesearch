from bungiesearch import Bungiesearch
from celery.task import Task as CeleryTask
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from importlib import import_module


def get_celery_task():
    ''' Helper method to get settings.CELERY_BUNGIESEARCH_CUSTOM_TASK.
        Default behavior (if not provided) is to use celery.Task.
    '''
    custom_task = getattr(settings, 'CELERY_BUNGIESEARCH_CUSTOM_TASK', False)
    if custom_task:
        celery_task = get_update_task(task_path=custom_task, as_class=True)
    else:
        celery_task = CeleryTask
    return celery_task


def get_update_task(task_path=None, as_class=False):
    ''' Helper function to get settings.CELERY_BUNGIESEARCH_TASK, or task_path,
        if provided.
    '''
    default_task_path = 'celery_bungiesearch.tasks.celeryindex.CeleryIndexTask'
    custom_task = getattr(settings, 'CELERY_BUNGIESEARCH_TASK', default_task_path)
    import_path = task_path or custom_task

    module, attr = import_path.rsplit('.', 1)
    try:
        mod = import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured('Error importing module %s: "%s"' % (module, e))
    try:
        Task = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a "%s" class.' % (module, attr))

    if as_class:
        return Task
    else:
        return Task()


def get_model_index(model):
    return Bungiesearch().get_model_index(model.__name__)


def get_model_indexing_query(model):
    return getattr(
        Bungiesearch().get_model_index(model.__name__).Meta,
        'indexing_query',
        model.objects.all()
    )
