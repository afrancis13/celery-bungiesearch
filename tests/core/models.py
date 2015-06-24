from bungiesearch.managers import BungiesearchManager
from django.db import models


class User(models.Model):
    name = models.TextField(db_index=True)
    user_id = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True)

    objects = BungiesearchManager()
