from bungiesearch.fields import DateField
from bungiesearch.indices import ModelIndex

from core.models import User


class UserIndex(ModelIndex):
    effective_date = DateField(
        eval_as='obj.created if obj.created and obj.updated > obj.created else obj.updated')

    class Meta:
        model = User
        updated_field = 'updated'
        indexing_query = User.objects.all().exclude(user_id='fake')
        default = True
