from bungiesearch import Bungiesearch
from bungiesearch.utils import update_index
from elasticsearch import TransportError
from elasticsearch.helpers import BulkIndexError

from .celerybungie import CeleryBungieTask


class BulkDeleteTask(CeleryBungieTask):

    def run(self, model, instance_pks, **kwargs):
        settings = Bungiesearch.BUNGIE.get('SIGNALS', {})
        buffer_size = settings.get('BUFFER_SIZE', 100)
        refresh = kwargs.get('refresh', self.refresh)

        try:
            update_index(instance_pks, model.__name__,
                action='delete', bulk_size=buffer_size, refresh=refresh)

        except BulkIndexError as e:
            for error in e.errors:
                if error['delete'] and error['delete']['status'] == 404:
                    continue
                raise

        except TransportError as e:
            if e.status_code == 404:
                return
            raise
