from django.db import models

from uuid import uuid4


class TarefaModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    done = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
  