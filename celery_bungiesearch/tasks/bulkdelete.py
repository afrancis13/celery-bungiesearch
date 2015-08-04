from .celerybungie import CeleryBungieTask
from bungiesearch import Bungiesearch
from bungiesearch.utils import update_index

from elasticsearch import TransportError


class BulkDeleteTask(CeleryBungieTask):

    def run(self, model, instances, **kwargs):
        settings = Bungiesearch.BUNGIE.get('SIGNALS', {})
        buffer_size = settings.get('BUFFER_SIZE', 100)

        try:
            update_index(instances, model.__name__, action='delete', bulk_size=buffer_size)
        except TransportError as e:
            if e.status_code == 404:
                return
            raise
