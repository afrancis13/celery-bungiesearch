from bungiesearch.utils import delete_index_item, update_index

from ..utils import get_model_indexing_query
from .celerybungie import CeleryBungieTask


class CeleryIndexTask(CeleryBungieTask):

    def run(self, action, instance, **kwargs):
        '''
        Trigger the actual index handler depending on the
        given action ('save', 'delete').
        '''
        model_class = type(instance)
        model_name = model_class.__name__

        if action not in ('save', 'delete'):
            raise ValueError('Unrecognized action: %s' % action)

        refresh = kwargs.get('refresh', self.refresh)

        if action == 'save':
            indexing_query = get_model_indexing_query(model_class)
            should_index = indexing_query.filter(pk=instance.pk).exists()

            if should_index:
                update_index([instance], model_name, refresh=refresh)
            else:
                delete_index_item(instance, model_name)

        elif action == 'delete':
            delete_index_item(instance, model_name, refresh=refresh)
