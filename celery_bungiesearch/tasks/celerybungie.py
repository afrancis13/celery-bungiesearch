from django.conf import settings

from ..utils import get_celery_task

CeleryTask = get_celery_task()


class CeleryBungieTask(CeleryTask):

    def delay(self, *args, **kwargs):
        if 'queue' not in kwargs and hasattr(settings, 'CELERY_BUNGIESEARCH_QUEUE'):
            kwargs['queue'] = settings.CELERY_BUNGIESEARCH_QUEUE

        super(CeleryBungieTask, self).delay(*args, **kwargs)
