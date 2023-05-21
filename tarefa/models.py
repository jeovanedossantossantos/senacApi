from django.db import models

from uuid import uuid4

from users.models import UsersModel


class TarefaModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    done = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)
    user=models.ForeignKey(UsersModel,on_delete=models.CASCADE,related_name="tarefa")
    create_at = models.DateTimeField(auto_now_add=True)
  