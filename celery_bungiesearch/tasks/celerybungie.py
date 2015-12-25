from django.conf import settings

from ..utils import get_celery_task

CeleryTask = get_celery_task()


class CeleryBungieTask(CeleryTask):

    refresh = False

    def delay(self, *args, **kwargs):
        if hasattr(settings, 'CELERY_BUNGIESEARCH_QUEUE') and 'queue' not in kwargs:
            kwargs['queue'] = settings.CELERY_BUNGIESEARCH_QUEUE

        super(CeleryBungieTask, self).delay(*args, **kwargs)
