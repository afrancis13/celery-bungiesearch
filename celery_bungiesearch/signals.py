from bungiesearch import Bungiesearch
from bungiesearch.signals import BungieSignalProcessor
from django.db.models import signals

from .enqueue import get_update_task


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

    def setup(self, model=None, models=[], setup_managed=False):
        connect_models = [model]
        if models:
            connect_models = models
        elif setup_managed:
            model_names = [mdl for index in Bungiesearch.get_indices()
                           for mdl in Bungiesearch.get_models(index)]
            connect_models = [Bungiesearch.get_model_index(model_str).get_model()
                              for model_str in model_names]

        for connect_model in connect_models:
            signals.post_save.connect(self.enqueue_save, sender=connect_model)
            signals.pre_delete.connect(self.enqueue_delete, sender=connect_model)

    def teardown(self, model=None, models=[], teardown_managed=False):
        disconnect_models = [model]
        if models:
            disconnect_models = models
        elif teardown_managed:
            model_names = [mdl for index in Bungiesearch.get_indices()
                           for mdl in Bungiesearch.get_models(index)]
            disconnect_models = [Bungiesearch.get_model_index(model_str).get_model()
                                 for model_str in model_names]

        for disconnect_model in disconnect_models:
            signals.pre_delete.disconnect(self.enqueue_delete, sender=disconnect_model)
            signals.post_save.disconnect(self.enqueue_save, sender=disconnect_model)
