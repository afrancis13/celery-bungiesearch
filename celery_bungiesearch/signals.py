from bungiesearch import Bungiesearch
from bungiesearch.signals import BungieSignalProcessor
from django.db.models.signals import post_save, pre_delete

from .utils import get_update_task


class CelerySignalProcessor(BungieSignalProcessor):

    ALLOWED_ACTIONS = ('save', 'delete')

    def enqueue_save(self, sender, instance, **kwargs):
        return self.enqueue('save', sender, instance, **kwargs)

    def enqueue_delete(self, sender, instance, **kwargs):
        return self.enqueue('delete', sender, instance, **kwargs)

    def enqueue(self, action, sender, instance, **kwargs):
        """
        Given an individual model instance, determine if a backend
        handles the model, check if the index is Celery-enabled and
        enqueue task.
        """
        try:
            Bungiesearch.get_index(sender, via_class=True)
        except KeyError:
            return  # This model is not managed by Bungiesearch.

        if action not in self.ALLOWED_ACTIONS:
            raise ValueError("Unrecognized action %s" % action)

        get_update_task().delay(action, instance)

    def setup(self, model):
        post_save.connect(self.enqueue_save, sender=model)
        pre_delete.connect(self.enqueue_delete, sender=model)

    def teardown(self, model):
        post_save.disconnect(self.enqueue_save, sender=model)
        pre_delete.disconnect(self.enqueue_delete, sender=model)
