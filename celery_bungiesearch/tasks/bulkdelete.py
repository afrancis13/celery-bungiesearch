from .celerybungie import CeleryBungieTask
from bungiesearch import Bungiesearch
from bungiesearch.utils import update_index


class BulkDeleteTask(CeleryBungieTask):

    def run(self, model, instances, **kwargs):
        settings = Bungiesearch.BUNGIE.get('SIGNALS', {})
        buffer_size = settings.get('BUFFER_SIZE', 100)
        update_index(instances, model.__name__, action='delete', bulk_size=buffer_size)
